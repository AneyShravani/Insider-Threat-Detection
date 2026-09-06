"""
prevention/engine.py
---------------------
The actual "decide and act" logic for the Prevention Engine.

Given a threat verdict (from the ML/alert side), this module decides:
  - should the user be suspended?
  - should the specific transfer/action be blocked?
and then carries out that decision (updating blocked-user status,
writing a prevention log entry).

Threat level can arrive as a string ("low" / "medium" / "high") or as a
numeric risk_score (0.0 - 1.0), matching what the ML model / dashboard
already produce elsewhere in this project.
"""

from prevention import db

KNOWN_TRANSFER_METHODS = {
    "email_send",
    "usb_copy",
    "usb_access",
    "cloud_upload",
    "printer_access",
    "database_export",
    "git_push",
    "network_share",
    "file_download",
}

# Transfer methods treated as sensitive enough to block outright even at
# MEDIUM threat level (based on the DLP dataset: these are the methods
# most associated with actual exfiltration incidents).
MEDIUM_RISK_BLOCK_METHODS = {"usb_copy", "cloud_upload", "email_send", "database_export"}


def normalize_threat_level(threat_level):
    """Accepts 'low'/'medium'/'high' (any case) or a numeric risk_score
    (0-1 or 0-100) and returns a canonical 'low' | 'medium' | 'high'."""
    if threat_level is None:
        raise ValueError("threat_level is required")

    if isinstance(threat_level, str) and not threat_level.replace(".", "", 1).isdigit():
        level = threat_level.strip().lower()
        if level not in ("low", "medium", "high"):
            raise ValueError(f"Unrecognized threat_level: {threat_level!r}")
        return level

    score = float(threat_level)
    if score > 1:  # allow 0-100 scale too
        score = score / 100.0
    if score >= 0.7:
        return "high"
    if score >= 0.4:
        return "medium"
    return "low"


def decide_action(threat_level, transfer_method=None):
    """Pure decision function - no side effects."""
    level = normalize_threat_level(threat_level)
    method = (transfer_method or "").strip().lower() or None

    if level == "high":
        return {
            "suspend_user": True,
            "block_transfer": True,
            "reason": "High threat level - user suspended and transfer blocked immediately.",
        }

    if level == "medium":
        if method in MEDIUM_RISK_BLOCK_METHODS:
            return {
                "suspend_user": False,
                "block_transfer": True,
                "reason": (
                    f"Medium threat level with sensitive transfer method "
                    f"'{method}' - transfer blocked, user flagged for monitoring."
                ),
            }
        return {
            "suspend_user": False,
            "block_transfer": False,
            "reason": "Medium threat level - allowed, flagged for monitoring.",
        }

    return {
        "suspend_user": False,
        "block_transfer": False,
        "reason": "Low threat level - normal activity, no action needed.",
    }


def block_user(user_id, reason, threat_level=None, blocked_by="system"):
    doc = {
        "user_id": user_id,
        "reason": reason,
        "threat_level": threat_level,
        "blocked_by": blocked_by,
        "blocked_at": db.now_iso(),
    }
    return db.upsert_blocked_user(doc)


def unblock_user(user_id, unblocked_by="system"):
    existed = db.remove_blocked_user(user_id)
    return existed


def get_status(user_id):
    record = db.get_blocked_user(user_id)
    if record:
        return {"user_id": user_id, "blocked": True, **{k: v for k, v in record.items() if k != "user_id"}}
    return {"user_id": user_id, "blocked": False}


def log_event(user_id, threat_level, action_taken, reason, file=None, action=None, transfer_method=None):
    doc = {
        "user_id": user_id,
        "file": file,
        "action": action or transfer_method,
        "transfer_method": transfer_method,
        "threat_level": threat_level,
        "reason": reason,
        "action_taken": action_taken,
    }
    return db.insert_log(doc)


def evaluate_threat(user_id, threat_level, file=None, action=None, transfer_method=None):
    """Main entry point: receive an ML/alert result and take real action."""
    if db.is_user_blocked(user_id):
        result = {
            "user_id": user_id,
            "threat_level": threat_level,
            "user_blocked": True,
            "transfer_blocked": True,
            "action_taken": "denied_already_blocked",
            "reason": "User is already suspended; action denied.",
        }
        log_event(
            user_id, threat_level, "denied_already_blocked", result["reason"],
            file=file, action=action, transfer_method=transfer_method,
        )
        return result

    decision = decide_action(threat_level, transfer_method)
    level = normalize_threat_level(threat_level)

    if decision["suspend_user"]:
        block_user(user_id, decision["reason"], threat_level=level)

    if decision["suspend_user"] and decision["block_transfer"]:
        action_taken = "blocked_transfer_and_suspended_user"
    elif decision["block_transfer"]:
        action_taken = "blocked_transfer"
    elif level == "medium":
        action_taken = "allowed_flagged"
    else:
        action_taken = "allowed"

    log_event(
        user_id, level, action_taken, decision["reason"],
        file=file, action=action, transfer_method=transfer_method,
    )

    return {
        "user_id": user_id,
        "threat_level": level,
        "user_blocked": decision["suspend_user"],
        "transfer_blocked": decision["block_transfer"],
        "action_taken": action_taken,
        "reason": decision["reason"],
    }