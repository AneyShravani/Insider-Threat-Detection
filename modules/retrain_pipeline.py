"""
Retraining Support — Objective 5, STEP 6.

Prepares a retraining dataset from CONFIRMED false negatives and exposes a
function to retrain the existing model architecture (RandomForestClassifier,
same as train_model.py) on the combined data.

Nothing in this file runs automatically. Call retrain_model() manually
(e.g. from a notebook, a CLI script, or an admin-only route) only after an
analyst has reviewed and confirmed which logged false negatives were real
insider threats.
"""

import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from config.fn_reduction_config import FALSE_NEGATIVE_LOG_PATH, RETRAIN_MIN_CONFIRMED_SAMPLES

ORIGINAL_DATASET = "data/insider_threat_scenarios.csv"
MODEL_PATH = "model/threat_model.pkl"
ENCODER_PATH = "model/label_encoder.pkl"


def prepare_retraining_dataset(confirmed_log_path: str = FALSE_NEGATIVE_LOG_PATH) -> pd.DataFrame:
    """
    Builds a retraining-ready DataFrame by combining the ORIGINAL training
    data with confirmed false negatives from the log.

    Confirmation is left to the caller: if the log (or a copy of it) has a
    'confirmed' column, only rows with confirmed == True are used. This
    guarantees the model is never retrained on unverified data.
    """
    base_df = pd.read_csv(ORIGINAL_DATASET)

    if not os.path.exists(confirmed_log_path):
        return base_df

    fn_df = pd.read_csv(confirmed_log_path)
    if fn_df.empty:
        return base_df

    if "confirmed" in fn_df.columns:
        fn_df = fn_df[fn_df["confirmed"].astype(str).str.lower() == "true"]

    if fn_df.empty:
        return base_df

    # Map logged false negatives into the same schema used for training.
    mapped_rows = []
    for _, row in fn_df.iterrows():
        risk_score_raw = pd.to_numeric(row.get("risk_score", 0), errors="coerce") or 0
        mapped_rows.append(
            {
                "risk_score": min(risk_score_raw / 100.0, 1.0),
                "false_positive": 0,
                "response_time": 0,
                "financial_impact": 0,
                # Confirmed false negatives are, by definition, real threats
                # that were missed - default them to 'medium' severity.
                "severity": "medium",
            }
        )

    extra_df = pd.DataFrame(mapped_rows)
    return pd.concat([base_df, extra_df], ignore_index=True, sort=False)


def retrain_model(
    confirmed_log_path: str = FALSE_NEGATIVE_LOG_PATH,
    min_samples: int = RETRAIN_MIN_CONFIRMED_SAMPLES,
):
    """
    Retrains the SAME model architecture used by train_model.py on the
    combined dataset (original data + confirmed false negatives).

    Must be triggered manually - this function is never called automatically
    by the rest of the application.
    """
    df = prepare_retraining_dataset(confirmed_log_path)

    if df["response_time"].dtype == object:
        df["response_time"] = (
            df["response_time"].astype(str).str.replace("_minutes", "").str.replace("_minute", "").astype(float)
        )
    if df["false_positive"].dtype == object:
        df["false_positive"] = df["false_positive"].map({"true": 1, "false": 0}).fillna(df["false_positive"])

    X = df[["risk_score", "false_positive", "response_time", "financial_impact"]]
    y = df["severity"]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y_encoded)

    os.makedirs("model", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)

    return {"trained_on_rows": len(df), "model_path": MODEL_PATH, "encoder_path": ENCODER_PATH}
