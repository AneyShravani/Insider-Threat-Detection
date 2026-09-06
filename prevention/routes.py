"""
prevention/routes.py
---------------------
Flask blueprint for the Prevention Engine.
"""

from flask import Blueprint, request, jsonify

from prevention import engine, db

prevention_bp = Blueprint("prevention", __name__, url_prefix="/prevention")


@prevention_bp.post("/evaluate")
def evaluate():
    """
    Body JSON:
    {
        "user_id": "U001",
        "threat_level": "high",
        "file": "financial_reports.xlsx",
        "action": "file_transfer",
        "transfer_method": "usb_copy"
    }
    """
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    threat_level = data.get("threat_level")

    if not user_id or threat_level is None:
        return jsonify({"error": "user_id and threat_level are required"}), 400

    try:
        result = engine.evaluate_threat(
            user_id=user_id,
            threat_level=threat_level,
            file=data.get("file"),
            action=data.get("action"),
            transfer_method=data.get("transfer_method"),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(result), 200


@prevention_bp.post("/block")
def block():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    reason = data.get("reason", "Manually blocked")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    doc = engine.block_user(
        user_id=user_id,
        reason=reason,
        threat_level=data.get("threat_level"),
        blocked_by=data.get("blocked_by", "system"),
    )
    engine.log_event(
        user_id, data.get("threat_level"), "user_suspended", reason,
        action="manual_block",
    )
    return jsonify({"message": f"User {user_id} blocked.", "record": doc}), 200


@prevention_bp.post("/unblock")
def unblock():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    existed = engine.unblock_user(user_id, unblocked_by=data.get("unblocked_by", "system"))

    if not existed:
        return jsonify({"message": f"User {user_id} was not blocked.", "was_blocked": False}), 200

    engine.log_event(
        user_id, None, "user_unblocked",
        f"Unblocked by {data.get('unblocked_by', 'system')}",
        action="manual_unblock",
    )
    return jsonify({"message": f"User {user_id} unblocked.", "was_blocked": True}), 200


@prevention_bp.get("/status/<user_id>")
def status(user_id):
    return jsonify(engine.get_status(user_id)), 200


@prevention_bp.get("/blocked-users")
def blocked_users():
    return jsonify(db.list_blocked_users()), 200


@prevention_bp.get("/logs")
def logs():
    user_id = request.args.get("user_id")
    threat_level = request.args.get("threat_level")
    limit = request.args.get("limit", default=100, type=int)
    return jsonify(db.get_logs(user_id=user_id, threat_level=threat_level, limit=limit)), 200