from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

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
    df = pd.read_csv('next work/insider_threat_scenarios.csv')
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
    df = pd.read_csv('next work/insider_threat_scenarios.csv')
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
    df = pd.read_csv('next work/insider_threat_scenarios.csv')
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
    df = pd.read_csv('next work/insider_threat_scenarios.csv')
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
    df = pd.read_csv('next work/ueba_data.csv')
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)