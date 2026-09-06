"""
Configuration for the False Negative Reduction Module (Objective 5).

Every threshold and weight used by the Risk Verification / False Negative
Reduction pipeline lives here so nothing is hardcoded inside the logic
files. Tune these values to retune the system without touching any other
code (STEP 2 / STEP 4 requirement: no hardcoded thresholds).
"""

# ---------------------------------------------------------------------------
# STEP 2 - Probability-based check (replaces the hardcoded 0.50 cut-off)
# ---------------------------------------------------------------------------
# The existing model is a multi-class classifier over `severity`
# ('low' / 'medium' / 'high'). The rest of the app already treats 'low' as
# "Normal / No Threat" (see app.py's /predict endpoint).
#
# THREAT_PROBABILITY_THRESHOLD is compared against (1 - P(severity='low')),
# i.e. how much probability mass the model placed OUTSIDE "Normal". If that
# exceeds the threshold, the case is treated as suspicious even though the
# model's top-1 prediction was "low".
THREAT_PROBABILITY_THRESHOLD = 0.35
NORMAL_SEVERITY_LABEL = "low"

# ---------------------------------------------------------------------------
# STEP 3 & 4 - Risk Verification / Risk Scoring
# ---------------------------------------------------------------------------
# Points added to the Risk Score whenever an indicator fires.
RISK_WEIGHTS = {
    "late_login": 20,
    "usb_activity": 25,
    "sensitive_file_access": 30,
    "mass_download": 15,
    "failed_logins": 10,
    "privilege_escalation": 25,
    "abnormal_application_usage": 15,
    "dlp_policy_violation": 20,
}

# A case predicted "Normal" by the ML model is escalated to
# "Potential Insider Threat" once the accumulated Risk Score reaches this.
RISK_SCORE_OVERRIDE_THRESHOLD = 40

# STEP 7 - Severity bands used to assign a severity once an override fires.
SEVERITY_BANDS = {
    "high": 60,
    "medium": 40,
    "low": 20,
}

# ---------------------------------------------------------------------------
# Rule parameters (configurable, not hardcoded inside the logic files)
# ---------------------------------------------------------------------------
BUSINESS_HOURS_START = 7            # 07:00 - before this counts as "late"
BUSINESS_HOURS_END = 19             # 19:00 - after this counts as "late"
FAILED_LOGIN_THRESHOLD = 3          # >= this many failed attempts fires the rule
MASS_DOWNLOAD_BYTES_THRESHOLD = 5_000_000  # 5 MB
SENSITIVE_DATA_TYPES = {
    "financial", "financial_data", "hr_data", "customer_data",
    "source_code", "payroll", "legal", "confidential", "research",
}
SUSPICIOUS_APPLICATIONS = {"Admin_Tool", "Screenshot_Tool", "Python_Script"}

# ---------------------------------------------------------------------------
# STEP 5 - False Negative logging
# ---------------------------------------------------------------------------
FALSE_NEGATIVE_LOG_PATH = "logs/false_negative_log.csv"

# ---------------------------------------------------------------------------
# STEP 6 - Retraining support
# ---------------------------------------------------------------------------
RETRAIN_MIN_CONFIRMED_SAMPLES = 10  # don't bother retraining below this
