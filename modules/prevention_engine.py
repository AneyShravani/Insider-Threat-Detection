"""
Objective 6 — Prevention Engine.

This module is additive: it does not change how threats are detected
(Objectives 1-5). It only reacts to a severity/threat_level that has
already been decided elsewhere, and turns that decision into an actual
action: blocking a user, restricting them, or letting the activity through.

Status model
------------
  low / normal  -> 🟢 normal      (no action)
  medium        -> 🟡 restricted  (flagged, activity limited, not fully blocked)
  high          -> 🔴 blocked     (user blocked, action/transfer stopped)
"""

from datetime import datetime, timezone
from modules.db import get_collection
from modules.notifier import send_admin_alert

blocked_users_col = get_collection("blocked_users")
logs_col = get_collection("prevention_logs")

STATUS_MAP = {
    "high": "blocked",
    "medium": "restricted",
    "low": "normal",
    "normal": "normal",
}


def _now():
    return datetime.now(timezone.utc).isoformat()


def get_status(user_id):
    """Returns the current prevention status for a user. Defaults to
    'normal' if the user has never been flagged."""
    doc = blocked_users_col.find_one({"user_id": user_id})
    if not doc:
        return {
            "user_id": user_id,
            "status": "normal",
            "reason": None,
            "threat_level": None,
            "updated_at": None,
        }
    return {
        "user_id": doc["user_id"],
        "status": doc["status"],
        "reason": doc.get("reason"),
        "threat_level": doc.get("threat_level"),
        "updated_at": doc.get("updated_at"),
    }


def is_blocked(user_id):
    return get_status(user_id)["status"] == "blocked"


def _log(user_id, action_taken, threat_level, reason, file_or_action=None,
          method=None, admin_triggered=False):
    entry = {
        "user_id": user_id,
        "file_or_action": file_or_action,
        "method": method,
        "threat_level": threat_level,
        "reason": reason,
        "action_taken": action_taken,
        "admin_triggered": admin_triggered,
        "timestamp": _now(),
    }
    logs_col.insert_one(dict(entry))
    return entry


def block_user(user_id, reason, threat_level="high", file_or_action=None,
               method=None, admin_triggered=False):
    """Sets (or updates) a user's prevention status and logs the action.
    threat_level drives the resulting status: high -> blocked,
    medium -> restricted. Admins calling this directly can still pass
    threat_level='high' to force a full block."""
    existing = blocked_users_col.find_one({"user_id": user_id})
    status = STATUS_MAP.get(threat_level, "blocked")

    record = {
        "user_id": user_id,
        "status": status,
        "reason": reason,
        "threat_level": threat_level,
        "updated_at": _now(),
    }

    if existing:
        blocked_users_col.update_one({"user_id": user_id}, {"$set": record})
    else:
        blocked_users_col.insert_one(dict(record))

    entry = _log(user_id, status, threat_level, reason, file_or_action, method, admin_triggered)

    if status == "blocked":
        send_admin_alert(
            subject=f"🔴 High-risk action blocked for {user_id}",
            body=(
                f"User: {user_id}\n"
                f"Reason: {reason}\n"
                f"Threat level: {threat_level}\n"
                f"File/Action: {file_or_action or 'N/A'}\n"
                f"Method: {method or 'N/A'}\n"
                f"Time: {entry['timestamp']}"
            ),
        )

    return record


def unblock_user(user_id, admin_id=None, note=None):
    """Restores a user to 'normal' status after admin verification."""
    existing = blocked_users_col.find_one({"user_id": user_id})
    reason = note or "Manually unblocked by admin after verification"

    record = {
        "user_id": user_id,
        "status": "normal",
        "reason": reason,
        "threat_level": None,
        "updated_at": _now(),
    }

    if existing:
        blocked_users_col.update_one({"user_id": user_id}, {"$set": record})
    else:
        blocked_users_col.insert_one(dict(record))

    _log(user_id, "unblocked", None, reason, admin_triggered=True)
    return record


def get_all_blocked():
    """Every user the prevention system has an opinion about (not just
    currently-blocked ones — includes restricted/normal history too)."""
    docs = blocked_users_col.find({})
    return [get_status(d["user_id"]) for d in docs]


def get_logs():
    logs = logs_col.find({})
    return sorted(logs, key=lambda x: x.get("timestamp", ""), reverse=True)


def evaluate_and_prevent(user_id, threat_level, reason, file_or_action=None, method=None):
    """The Threat -> Prevention trigger. Call this with the severity that
    Objectives 1/5 already produced; this function decides whether
    prevention should happen, and if so, does it.

    Idempotent: if the user is already sitting at the same status for the
    same threat_level, it won't write a duplicate log entry every time the
    same detection is re-evaluated (e.g. a dashboard refresh) — it only
    logs on an actual change of state.
    """
    status = STATUS_MAP.get(threat_level, "normal")

    if status == "normal":
        return {"action_prevented": False, "status": "normal"}

    current = get_status(user_id)
    if current["status"] == status and current["threat_level"] == threat_level:
        return {
            "action_prevented": status == "blocked",
            "status": status,
            "record": current,
            "already_actioned": True,
        }

    record = block_user(
        user_id=user_id,
        reason=reason,
        threat_level=threat_level,
        file_or_action=file_or_action,
        method=method,
        admin_triggered=False,
    )
    return {"action_prevented": status == "blocked", "status": status, "record": record}


def check_file_transfer(user_id, file_name, method, threat_level):
    """File-transfer / exfiltration prevention hook. Supports whatever
    transfer method is passed in (usb, email, cloud_upload, network_share,
    ftp, etc.) — the method is just recorded and doesn't change the
    blocking decision, since risk is driven by threat_level either way."""
    decision = evaluate_and_prevent(
        user_id=user_id,
        threat_level=threat_level,
        reason=f"Suspicious file transfer detected via {method}",
        file_or_action=file_name,
        method=method,
    )
    blocked = decision["status"] == "blocked"
    return {
        "user_id": user_id,
        "file_name": file_name,
        "method": method,
        "threat_level": threat_level,
        "transfer_allowed": not blocked,
        "action": "blocked" if blocked else decision["status"],
    }
