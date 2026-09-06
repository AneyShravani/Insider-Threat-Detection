"""
Risk Verification Module — Objective 5, STEP 3 & STEP 4.

Even when the existing ML model predicts "Normal" (severity == 'low'),
this module inspects behavioural indicators that are ALREADY present in
the project's existing datasets (UEBA, PAM, DLP) and produces a
configurable Risk Score. It never retrains or touches the existing model
- it is a purely additive verification layer.
"""

import os
import pandas as pd

from config.fn_reduction_config import (
    RISK_WEIGHTS,
    BUSINESS_HOURS_START,
    BUSINESS_HOURS_END,
    FAILED_LOGIN_THRESHOLD,
    MASS_DOWNLOAD_BYTES_THRESHOLD,
    SENSITIVE_DATA_TYPES,
    SUSPICIOUS_APPLICATIONS,
)

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA_DIR = os.path.join(os.path.dirname(_THIS_DIR), "data")


class RiskVerificationEngine:
    """
    Reuses the project's existing UEBA / PAM / DLP datasets to compute a
    behavioural Risk Score for a given user_id, independent of the ML
    model's own prediction.
    """

    def __init__(self, data_dir: str = DEFAULT_DATA_DIR):
        self.data_dir = data_dir
        self._ueba = self._safe_read("ueba_data.csv")
        self._pam = self._safe_read("pam_data.csv")
        self._dlp = self._safe_read("dlp_events.csv")

    def _safe_read(self, filename):
        path = os.path.join(self.data_dir, filename)
        if os.path.exists(path):
            try:
                return pd.read_csv(path)
            except Exception:
                return pd.DataFrame()
        return pd.DataFrame()

    @staticmethod
    def _rows_for_user(df, user_id):
        if df.empty or "user_id" not in df.columns:
            return pd.DataFrame()
        return df[df["user_id"] == user_id]

    # ---- individual indicator checks (STEP 3) -----------------------------

    def _check_late_login(self, user_ueba):
        if user_ueba.empty or "login_time" not in user_ueba:
            return False
        for ts in user_ueba["login_time"].dropna().unique():
            try:
                hour = pd.to_datetime(ts, dayfirst=True).hour
            except Exception:
                continue
            if hour < BUSINESS_HOURS_START or hour >= BUSINESS_HOURS_END:
                return True
        return False

    def _check_usb_activity(self, user_ueba, user_dlp):
        usb_ueba = (
            not user_ueba.empty
            and "activity_type" in user_ueba
            and (user_ueba["activity_type"] == "usb_access").any()
        )
        usb_dlp = (
            not user_dlp.empty
            and "action" in user_dlp
            and (user_dlp["action"] == "usb_copy").any()
        )
        return bool(usb_ueba or usb_dlp)

    def _check_sensitive_file_access(self, user_ueba, user_dlp):
        sensitive_ueba = (
            not user_ueba.empty
            and "data_type" in user_ueba
            and user_ueba["data_type"].isin(SENSITIVE_DATA_TYPES).any()
        )
        sensitive_dlp = (
            not user_dlp.empty
            and "data_classification" in user_dlp
            and (user_dlp["data_classification"] == "confidential").any()
        )
        return bool(sensitive_ueba or sensitive_dlp)

    def _check_mass_download(self, user_ueba, user_dlp):
        mass_ueba = (
            not user_ueba.empty
            and "file_size" in user_ueba
            and (user_ueba["file_size"].fillna(0) >= MASS_DOWNLOAD_BYTES_THRESHOLD).any()
        )
        mass_dlp = (
            not user_dlp.empty
            and "file_size" in user_dlp
            and (user_dlp["file_size"].fillna(0) >= MASS_DOWNLOAD_BYTES_THRESHOLD).any()
        )
        return bool(mass_ueba or mass_dlp)

    def _check_failed_logins(self, user_ueba):
        # `success_status` exists today but the current dataset only ever
        # contains 'success'. This rule is future-proof: it starts firing
        # automatically the moment failed-login records appear.
        if user_ueba.empty or "success_status" not in user_ueba:
            return False
        failed = (user_ueba["success_status"] != "success").sum()
        return failed >= FAILED_LOGIN_THRESHOLD

    def _check_privilege_escalation(self, user_pam):
        if user_pam.empty or "privilege_escalation" not in user_pam:
            return False
        return user_pam["privilege_escalation"].astype(str).str.lower().eq("true").any()

    def _check_abnormal_application_usage(self, user_ueba):
        if user_ueba.empty or "application_used" not in user_ueba:
            return False
        return user_ueba["application_used"].isin(SUSPICIOUS_APPLICATIONS).any()

    def _check_dlp_policy_violation(self, user_dlp):
        if user_dlp.empty or "policy_violation" not in user_dlp:
            return False
        return user_dlp["policy_violation"].notna().any()

    # ---- public API (STEP 4) ----------------------------------------------

    def compute_risk_score(self, user_id: str):
        """
        Returns (total_score: int, triggered_rules: list[str]) for the
        given user_id, using only data already present in the project's
        existing datasets.
        """
        user_ueba = self._rows_for_user(self._ueba, user_id)
        user_pam = self._rows_for_user(self._pam, user_id)
        user_dlp = self._rows_for_user(self._dlp, user_id)

        rule_results = {
            "late_login": self._check_late_login(user_ueba),
            "usb_activity": self._check_usb_activity(user_ueba, user_dlp),
            "sensitive_file_access": self._check_sensitive_file_access(user_ueba, user_dlp),
            "mass_download": self._check_mass_download(user_ueba, user_dlp),
            "failed_logins": self._check_failed_logins(user_ueba),
            "privilege_escalation": self._check_privilege_escalation(user_pam),
            "abnormal_application_usage": self._check_abnormal_application_usage(user_ueba),
            "dlp_policy_violation": self._check_dlp_policy_violation(user_dlp),
        }

        triggered_rules = [rule for rule, fired in rule_results.items() if fired]
        total_score = sum(RISK_WEIGHTS.get(rule, 0) for rule in triggered_rules)
        return total_score, triggered_rules
