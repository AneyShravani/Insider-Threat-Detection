#test

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

# ── Objective 5: False Negative Reduction (additive, does not touch the
#    existing model / prediction logic above) ──────────────────────────
from modules.false_negative_reducer import verify_prediction
from modules.false_negative_logger import read_false_negative_log
from modules.retrain_pipeline import prepare_retraining_dataset

# ── Objective 6: Prevention Engine (additive, does not touch existing
#    detection / alerting / false-negative logic above) ────────────────
from modules.prevention_engine import (
    block_user,
    unblock_user,
    get_status,
    get_all_blocked,
    get_logs,
    evaluate_and_prevent,
    check_file_transfer,
)
from modules.notifier import get_notification_log

app = Flask(__name__)
CORS(app)

model = joblib.load('model/threat_model.pkl')
le    = joblib.load('model/label_encoder.pkl')

@app.route('/')
def home():
    return "Insider Threat Detection API is running!"

# ── Alerts endpoint for Dashboard ────────────────────────────
@app.route('/alerts')
def get_alerts():
    df = pd.read_csv('data/insider_threat_scenarios.csv')
    df['response_time'] = df['response_time'].str.replace('_minutes', '').str.replace('_minute', '').astype(float)
    df['false_positive'] = df['false_positive'].map({'true': 1, 'false': 0})

    features = df[['risk_score', 'false_positive', 'response_time', 'financial_impact']]
    predictions = model.predict(features)
    severities = le.inverse_transform(predictions)

    alerts = []
    for i, row in df.iterrows():
        alerts.append({
            'user': row['user_id'],
            'threat_type': row['threat_type'],
            'risk': round(row['risk_score'] * 100),
            'severity': severities[i],
            'financial_impact': row['financial_impact']
        })

    return jsonify(alerts)

# ── Predict endpoint for Investigation ───────────────────────
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    risk_score       = float(data['risk_score'])
    false_positive   = int(data['false_positive'])
    response_time    = float(data['response_time'])
    financial_impact = float(data['financial_impact'])

    features = [[risk_score, false_positive, response_time, financial_impact]]
    prediction = model.predict(features)
    severity = le.inverse_transform(prediction)[0]

    color_map = {'low': '#22c55e', 'medium': '#f97316', 'high': '#ef4444'}

    return jsonify({
        'severity': severity,
        'color': color_map.get(severity, 'gray'),
        'message': f'Insider Threat Detected! Severity: {severity.upper()}'
                   if severity != 'low' else 'Normal Behavior Detected'
    })

# ── Users endpoint ────────────────────────────────────────────
@app.route('/users')
def get_users():
    df = pd.read_csv('data/insider_threat_scenarios.csv')
    df['response_time'] = df['response_time'].str.replace('_minutes','').str.replace('_minute','').astype(float)
    df['false_positive'] = df['false_positive'].map({'true': 1, 'false': 0})

    features = df[['risk_score', 'false_positive', 'response_time', 'financial_impact']]
    predictions = model.predict(features)
    severities = le.inverse_transform(predictions)

    users = []
    for i, row in df.iterrows():
        users.append({
            'user_id': row['user_id'],
            'threat_type': row['threat_type'],
            'risk_score': row['risk_score'],
            'severity': severities[i],
            'mitigation': row['mitigation_action'],
            'outcome': row['outcome']
        })
    return jsonify(users)

# ── Timeline endpoint ─────────────────────────────────────────
@app.route('/timeline')
def get_timeline():
    df = pd.read_csv('data/insider_threat_scenarios.csv')
    timeline = []
    for _, row in df.iterrows():
        timeline.append({
            'user_id': row['user_id'],
            'threat_type': row['threat_type'],
            'severity': row['severity'],
            'detection_time': row['detection_time'],
            'outcome': row['outcome'],
            'risk_score': row['risk_score']
        })
    return jsonify(timeline)

# ── Reports endpoint ──────────────────────────────────────────
@app.route('/report-summary')
def get_report():
    df = pd.read_csv('data/insider_threat_scenarios.csv')
    df['response_time'] = df['response_time'].str.replace('_minutes','').str.replace('_minute','').astype(float)
    df['false_positive'] = df['false_positive'].map({'true': 1, 'false': 0})

    features = df[['risk_score', 'false_positive', 'response_time', 'financial_impact']]
    predictions = model.predict(features)
    severities = le.inverse_transform(predictions)

    total = len(df)
    high   = int((severities == 'high').sum())
    medium = int((severities == 'medium').sum())
    low    = int((severities == 'low').sum())

    return jsonify({
        'total_threats': total,
        'high': high,
        'medium': medium,
        'low': low,
        'total_financial_impact': int(df['financial_impact'].sum()),
        'most_common_threat': df['threat_type'].mode()[0],
        'false_positives': int(df['false_positive'].sum())
    })

# ── Behavior Analysis endpoint ────────────────────────────────
@app.route('/behavior')
def get_behavior():
    df = pd.read_csv('data/ueba_data.csv')
    df['anomaly'] = df['risk_score'].apply(lambda x: True if x > 0.7 else False)

    user_summary = []
    for user in df['user_id'].unique():
        user_df = df[df['user_id'] == user]
        user_summary.append({
            'user_id': user,
            'total_activities': len(user_df),
            'avg_risk_score': round(float(user_df['risk_score'].mean()), 2),
            'anomalies_detected': int(user_df['anomaly'].sum()),
            'most_common_activity': user_df['activity_type'].mode()[0],
            'data_types_accessed': int(user_df['data_type'].nunique()),
            'locations': user_df['location'].unique().tolist()
        })

    return jsonify(user_summary)


#charts

@app.route('/api/dashboard')
def dashboard():
    return jsonify({
        "threat_severity": [
            {"name": "High", "value": 43.3},
            {"name": "Medium", "value": 40.0},
            {"name": "Low", "value": 16.7}
        ],
        "detections_by_hour": [
            {"hour": 8, "count": 4},
            {"hour": 9, "count": 3},
            {"hour": 10, "count": 5},
            {"hour": 11, "count": 3},
            {"hour": 12, "count": 3},
            {"hour": 13, "count": 2},
            {"hour": 14, "count": 3},
            {"hour": 15, "count": 1},
            {"hour": 16, "count": 3},
            {"hour": 17, "count": 1}
        ],
        "dlp_violations": [
            {"name": "High", "count": 14},
            {"name": "Medium", "count": 10},
            {"name": "Low", "count": 6}
        ]
    })

@app.route('/api/threats')
def threats():
    return jsonify({
        "top_threats": [
            {"name": "data_exfiltration", "count": 1},
            {"name": "privilege_abuse", "count": 1},
            {"name": "code_theft", "count": 1},
            {"name": "data_theft", "count": 1},
            {"name": "payroll_fraud", "count": 1},
            {"name": "normal_activity", "count": 1},
            {"name": "research_misconduct", "count": 1},
            {"name": "network_sabotage", "count": 1},
            {"name": "legal_breach", "count": 1},
            {"name": "competitive_intelligence", "count": 1}
        ],
        "network_protocols": [
            {"name": "SMB", "value": 28.2},
            {"name": "SSH", "value": 23.1},
            {"name": "HTTPS", "value": 17.9},
            {"name": "HTTP", "value": 10.3},
            {"name": "MySQL", "value": 7.7},
            {"name": "SMTP", "value": 5.1},
            {"name": "DNS", "value": 2.6},
            {"name": "IPP", "value": 2.6},
            {"name": "RDP", "value": 2.6}
        ]
    })

@app.route('/api/user-risk')
def user_risk():
    return jsonify({
        "risky_users": [
            {"user": "U006", "score": 0.55},
            {"user": "U002", "score": 0.52},
            {"user": "U007", "score": 0.50},
            {"user": "U010", "score": 0.48},
            {"user": "U003", "score": 0.45},
            {"user": "U009", "score": 0.43},
            {"user": "U001", "score": 0.40},
            {"user": "U005", "score": 0.38},
            {"user": "U004", "score": 0.35},
            {"user": "U008", "score": 0.30}
        ],
        "pam_risk": [
            {"name": "High", "value": 51.6},
            {"name": "Medium", "value": 22.6},
            {"name": "Low", "value": 25.8}
        ]
    })

@app.route('/api/ml-analysis')
def ml_analysis():
    return jsonify({
        "feature_importance": [
            {"feature": "UEBA Risk", "score": 0.35},
            {"feature": "Network Activity", "score": 0.25},
            {"feature": "PAM Events", "score": 0.20},
            {"feature": "DLP Violations", "score": 0.20}
        ],
        "malware_confidence": [
            {"score": 0.60, "count": 1},
            {"score": 0.65, "count": 1},
            {"score": 0.70, "count": 3},
            {"score": 0.75, "count": 4},
            {"score": 0.80, "count": 4},
            {"score": 0.85, "count": 6},
            {"score": 0.90, "count": 4},
            {"score": 0.95, "count": 4}
        ]
    })


@app.route('/api/behavior-charts')
def behavior_charts():
    return jsonify({
        "ueba_activity": [
            {"activity": "file_access", "count": 11},
            {"activity": "login", "count": 10},
            {"activity": "email_send", "count": 2},
            {"activity": "usb_access", "count": 2},
            {"activity": "cloud_upload", "count": 1},
            {"activity": "printer_access", "count": 1},
            {"activity": "git_push", "count": 1},
            {"activity": "database_export", "count": 1}
        ],
        "malware_impact": [
            {"level": "High", "count": 18},
            {"level": "Medium", "count": 17},
            {"level": "Low", "count": 1}
        ]
    })

@app.route('/api/investigation-charts')
def investigation_charts():
    df = pd.read_csv('data/insider_threat_scenarios.csv')
    df['response_time'] = df['response_time'].str.replace('_minutes','').str.replace('_minute','').astype(float)

    # Risk Score vs Financial Impact
    scatter = []
    for _, row in df.iterrows():
        scatter.append({
            "risk_score": round(float(row['risk_score']), 2),
            "financial_impact": int(row['financial_impact'])
        })

    return jsonify({
        "scatter": scatter,
        "correlation": [
            {"feature": "ueba_avg_risk",   "ueba_avg_risk": 1.0,  "network_bytes": 0.22, "pam_events": 0.97, "dlp_violations": 0.84, "risk_score": 0.023},
            {"feature": "network_bytes",   "ueba_avg_risk": 0.22, "network_bytes": 1.0,  "pam_events": 0.16, "dlp_violations": 0.16, "risk_score": 0.15},
            {"feature": "pam_events",      "ueba_avg_risk": 0.97, "network_bytes": 0.16, "pam_events": 1.0,  "dlp_violations": 0.8,  "risk_score": 0.034},
            {"feature": "dlp_violations",  "ueba_avg_risk": 0.84, "network_bytes": 0.16, "pam_events": 0.8,  "dlp_violations": 1.0,  "risk_score": -0.065},
            {"feature": "risk_score",      "ueba_avg_risk": 0.023,"network_bytes": 0.15, "pam_events": 0.034,"dlp_violations": -0.065,"risk_score": 1.0}
        ]
    })

@app.route('/api/report-charts')
def report_charts():
    df = pd.read_csv('data/insider_threat_scenarios.csv')

    # Top 10 Financial Impact Scenarios
    top_financial = df[['scenario_id', 'financial_impact']]\
        .sort_values('financial_impact', ascending=False)\
        .head(10)\
        .rename(columns={'scenario_id': 'scenario', 'financial_impact': 'impact'})\
        .to_dict(orient='records')

    # Escalation Requirements
    escalation = df['escalation_path'].value_counts().reset_index()
    escalation.columns = ['name', 'value']
    escalation_list = escalation.to_dict(orient='records')

    # Top 10 Threat Types
    threat_types = df['threat_type'].value_counts().reset_index()
    threat_types.columns = ['threat', 'count']
    threat_list = threat_types.head(10).to_dict(orient='records')

    # Risk Score Distribution (buckets)
    bins = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    labels = ['0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9']
    df['risk_bucket'] = pd.cut(df['risk_score'], bins=bins, labels=labels, include_lowest=True)
    risk_dist = df['risk_bucket'].value_counts().sort_index().reset_index()
    risk_dist.columns = ['score', 'frequency']
    risk_list = risk_dist.to_dict(orient='records')

    return jsonify({
        "top_financial": top_financial,
        "escalation": escalation_list,
        "threat_types": threat_list,
        "risk_distribution": risk_list
    })

# ══════════════════════════════════════════════════════════════════════
# Objective 5 — False Negative Reduction endpoints
# These are NEW routes only. Every route above is untouched, so existing
# functionality (/alerts, /predict, /users, /timeline, etc.) keeps working
# exactly as before.
# ══════════════════════════════════════════════════════════════════════

# ── Same data as /alerts, plus the False Negative Reduction verdict ────
@app.route('/alerts-verified')
def get_alerts_verified():
    df = pd.read_csv('data/insider_threat_scenarios.csv')
    df['response_time'] = df['response_time'].str.replace('_minutes', '').str.replace('_minute', '').astype(float)
    df['false_positive'] = df['false_positive'].map({'true': 1, 'false': 0})

    features = df[['risk_score', 'false_positive', 'response_time', 'financial_impact']]

    # STEP 1: existing ML prediction, completely unchanged.
    predictions = model.predict(features)
    severities = le.inverse_transform(predictions)

    # STEP 2: probability scores, if the model supports predict_proba().
    proba_matrix = model.predict_proba(features) if hasattr(model, 'predict_proba') else None
    class_labels = le.inverse_transform(model.classes_) if proba_matrix is not None else None

    alerts = []
    for i, row in df.iterrows():
        ml_severity = severities[i]

        probability_by_class = {}
        if proba_matrix is not None:
            probability_by_class = dict(zip(class_labels, proba_matrix[i]))

        verdict = verify_prediction(
            user_id=row['user_id'],
            ml_severity=ml_severity,
            probability_by_class=probability_by_class,
        )

        # ── Objective 6: Threat -> Prevention trigger ──
        prevention = evaluate_and_prevent(
            user_id=row['user_id'],
            threat_level=verdict['final_severity'],
            reason=f"Threat detected: {row['threat_type']}",
            file_or_action=row['threat_type'],
        )

        alerts.append({
            # ── original /alerts fields, unchanged ──
            'user': row['user_id'],
            'threat_type': row['threat_type'],
            'risk': round(row['risk_score'] * 100),
            'severity': ml_severity,
            'financial_impact': row['financial_impact'],
            # ── new Objective 5 fields ──
            'fn_final_decision': verdict['final_decision'],
            'fn_final_severity': verdict['final_severity'],
            'fn_overridden': verdict['overridden'],
            'fn_risk_score': verdict['risk_score'],
            'fn_triggered_rules': verdict['triggered_rules'],
            'fn_probability_threat': verdict['probability_threat'],
            # ── new Objective 6 fields ──
            'action_prevented': prevention['action_prevented'],
            'prevention_status': prevention['status'],
        })

    return jsonify(alerts)


# ── Same input as /predict, plus user_id so the verification layer can
#    look up that user's UEBA/PAM/DLP indicators ───────────────────────
@app.route('/predict-verified', methods=['POST'])
def predict_verified():
    data = request.json
    user_id           = data.get('user_id', 'UNKNOWN')
    risk_score        = float(data['risk_score'])
    false_positive    = int(data['false_positive'])
    response_time     = float(data['response_time'])
    financial_impact  = float(data['financial_impact'])

    features = [[risk_score, false_positive, response_time, financial_impact]]

    # STEP 1: existing ML prediction, completely unchanged.
    prediction = model.predict(features)
    ml_severity = le.inverse_transform(prediction)[0]

    # STEP 2: probability scores, if supported.
    probability_by_class = {}
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(features)[0]
        class_labels = le.inverse_transform(model.classes_)
        probability_by_class = dict(zip(class_labels, proba))

    # STEP 3-5: risk verification, scoring, override decision, logging.
    verdict = verify_prediction(user_id, ml_severity, probability_by_class)

    color_map = {'low': '#22c55e', 'medium': '#f97316', 'high': '#ef4444'}
    final_severity = verdict['final_severity']

    # ── Objective 6: Threat -> Prevention trigger ──
    prevention = evaluate_and_prevent(
        user_id=user_id,
        threat_level=final_severity,
        reason="Threat detected via manual prediction check",
    )

    return jsonify({
        'ml_severity': ml_severity,                      # unchanged original prediction
        'final_severity': final_severity,                # after false-negative verification
        'color': color_map.get(final_severity, 'gray'),
        'overridden': verdict['overridden'],
        'risk_score': verdict['risk_score'],
        'triggered_rules': verdict['triggered_rules'],
        'probability_threat': verdict['probability_threat'],
        'action_prevented': prevention['action_prevented'],
        'prevention_status': prevention['status'],
        'message': (
            f"Insider Threat Detected! Severity: {final_severity.upper()}"
            if verdict['final_decision'] != 'Normal'
            else 'Normal Behavior Detected'
        ),
    })


# ── View everything the False Negative module has caught so far ───────
@app.route('/false-negatives')
def get_false_negatives():
    return jsonify(read_false_negative_log())


# ══════════════════════════════════════════════════════════════════════
# Objective 6 — Prevention Engine
# All routes below are new/additive. Nothing above this section was
# changed in behavior, only the two /alerts-verified and /predict-verified
# routes now also call evaluate_and_prevent() (see the small blocks added
# above), so /alerts, /predict, /users, /timeline, etc. still work exactly
# as before.
# ══════════════════════════════════════════════════════════════════════

@app.route('/prevention/block', methods=['POST'])
def prevention_block():
    """Admin (or automated caller) manually blocks/restricts a user."""
    data = request.json or {}
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    reason        = data.get('reason', 'Manually blocked by admin')
    threat_level  = data.get('threat_level', 'high')
    file_or_action = data.get('file_or_action')
    method        = data.get('method')

    record = block_user(
        user_id=user_id,
        reason=reason,
        threat_level=threat_level,
        file_or_action=file_or_action,
        method=method,
        admin_triggered=True,
    )
    return jsonify({'message': f"User {user_id} status set to '{record['status']}'", 'record': record})


@app.route('/prevention/unblock', methods=['POST'])
def prevention_unblock():
    """Admin unblocks a user after manual verification."""
    data = request.json or {}
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    admin_id = data.get('admin_id', 'admin')
    note     = data.get('note')

    record = unblock_user(user_id, admin_id=admin_id, note=note)
    return jsonify({'message': f'User {user_id} unblocked', 'record': record})


@app.route('/prevention/status/<user_id>')
def prevention_status(user_id):
    """Current prevention status for a single user."""
    return jsonify(get_status(user_id))


@app.route('/prevention/blocked-users')
def prevention_blocked_users():
    """Every user the prevention system has a status for (normal/restricted/blocked)."""
    return jsonify(get_all_blocked())


@app.route('/prevention/logs')
def prevention_logs():
    """Full prevention action log: user, file/action, threat level, reason,
    timestamp, action taken."""
    return jsonify(get_logs())


@app.route('/prevention/check-transfer', methods=['POST'])
def prevention_check_transfer():
    """File-transfer prevention check. Accepts any transfer method
    (usb, email, cloud_upload, network_share, ftp, ...). Blocks the
    transfer when the associated threat_level is 'high'."""
    data = request.json or {}
    user_id      = data.get('user_id')
    file_name    = data.get('file_name', 'unknown_file')
    method       = data.get('method', 'unknown')
    threat_level = data.get('threat_level', 'low')

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    result = check_file_transfer(user_id, file_name, method, threat_level)
    return jsonify(result)


@app.route('/prevention/notifications')
def prevention_notifications():
    """Admin notification log (real emails if SMTP_* env vars are set,
    otherwise simulated/logged notifications)."""
    return jsonify(get_notification_log())


if __name__ == '__main__':
    app.run(debug=True, port=5000)