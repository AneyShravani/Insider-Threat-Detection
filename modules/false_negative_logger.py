"""
False Negative Logging — Objective 5, STEP 5.

Whenever the ML model says "Normal" but the Risk Verification Module
disagrees, the event is appended to logs/false_negative_log.csv so it can
be reviewed by an analyst and later used for retraining
(see modules/retrain_pipeline.py).
"""

import os
import csv
from datetime import datetime

from config.fn_reduction_config import FALSE_NEGATIVE_LOG_PATH

_FIELDNAMES = [
    "timestamp",
    "user_id",
    "ml_prediction",
    "probability_threat",
    "risk_score",
    "triggered_rules",
    "final_decision",
]


def log_false_negative(
    user_id,
    ml_prediction,
    probability_threat,
    risk_score,
    triggered_rules,
    final_decision,
    log_path: str = FALSE_NEGATIVE_LOG_PATH,
):
    """Append one confirmed-by-the-verification-layer false negative to the log."""
    log_dir = os.path.dirname(log_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    file_exists = os.path.exists(log_path)

    with open(log_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "user_id": user_id,
                "ml_prediction": ml_prediction,
                "probability_threat": round(probability_threat, 4) if probability_threat is not None else "",
                "risk_score": risk_score,
                "triggered_rules": "+".join(triggered_rules) if triggered_rules else "",
                "final_decision": final_decision,
            }
        )


def read_false_negative_log(log_path: str = FALSE_NEGATIVE_LOG_PATH):
    """Return all logged false-negative events as a list of dicts (empty list if none yet)."""
    if not os.path.exists(log_path):
        return []
    with open(log_path, mode="r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
