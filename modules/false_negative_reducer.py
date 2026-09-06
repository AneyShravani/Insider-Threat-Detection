"""
False Negative Reduction Module — Objective 5 orchestrator (STEP 1-5, 7).

Sits AFTER the existing ML prediction and never modifies it. It:

 1. Accepts the existing model's unmodified prediction + predict_proba output
 2. Applies a configurable probability threshold (replacing a hardcoded 0.50)
 3. Runs the RiskVerificationEngine over the project's existing datasets
 4. Combines both signals: if the model said "Normal" but either signal
    disagrees, the case is escalated to "Potential Insider Threat"
 5. Logs every such false negative for later review / retraining
 6. Produces a severity using the same low/medium/high convention already
    used throughout the app, so it can be dropped straight into the
    existing alert system
"""

from config.fn_reduction_config import (
    THREAT_PROBABILITY_THRESHOLD,
    NORMAL_SEVERITY_LABEL,
    RISK_SCORE_OVERRIDE_THRESHOLD,
    SEVERITY_BANDS,
)
from modules.risk_verification import RiskVerificationEngine
from modules.false_negative_logger import log_false_negative

# Built once and reused - loads the existing datasets a single time.
_engine = RiskVerificationEngine()


def _severity_from_risk_score(score: int) -> str:
    if score >= SEVERITY_BANDS["high"]:
        return "high"
    if score >= SEVERITY_BANDS["medium"]:
        return "medium"
    return "low"


def verify_prediction(user_id: str, ml_severity: str, probability_by_class: dict):
    """
    Core STEP 1-5 orchestration.

    Parameters
    ----------
    user_id : str
        The user this prediction concerns.
    ml_severity : str
        The UNCHANGED top-1 output of the existing ML model
        ('low' / 'medium' / 'high'). Never altered by this function.
    probability_by_class : dict
        {class_label: probability} straight from the existing model's
        predict_proba(), or {} if the model doesn't support it.

    Returns
    -------
    dict with the original ML prediction plus the verified, final decision.
    """
    prob_normal = probability_by_class.get(NORMAL_SEVERITY_LABEL)
    prob_threat = (1 - prob_normal) if prob_normal is not None else None

    risk_score, triggered_rules = _engine.compute_risk_score(user_id)

    probability_flag = prob_threat is not None and prob_threat >= THREAT_PROBABILITY_THRESHOLD
    risk_flag = risk_score >= RISK_SCORE_OVERRIDE_THRESHOLD

    # A false negative is a case the ML model called "Normal" that either
    # verification signal disagrees with.
    is_false_negative = ml_severity == NORMAL_SEVERITY_LABEL and (probability_flag or risk_flag)

    if is_false_negative:
        final_decision = "Potential Insider Threat"
        final_severity = _severity_from_risk_score(risk_score) if risk_flag else "low"
        log_false_negative(
            user_id=user_id,
            ml_prediction=ml_severity,
            probability_threat=prob_threat,
            risk_score=risk_score,
            triggered_rules=triggered_rules,
            final_decision=final_decision,
        )
    else:
        final_decision = "Normal" if ml_severity == NORMAL_SEVERITY_LABEL else "Insider Threat"
        final_severity = ml_severity

    return {
        "user_id": user_id,
        "ml_prediction": ml_severity,          # untouched original prediction
        "probability_threat": prob_threat,
        "risk_score": risk_score,
        "triggered_rules": triggered_rules,
        "overridden": is_false_negative,
        "final_decision": final_decision,
        "final_severity": final_severity,      # feed this into alert severity
    }
