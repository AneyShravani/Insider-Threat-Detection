import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load dataset
df = pd.read_csv('next work/insider_threat_scenarios.csv')

# Clean columns
df['response_time'] = df['response_time'].str.replace('_minutes', '').str.replace('_minute', '').astype(float)
df['false_positive'] = df['false_positive'].map({'true': 1, 'false': 0})

# Features and target
X = df[['risk_score', 'false_positive', 'response_time', 'financial_impact']]
y = df['severity']

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/threat_model.pkl')
joblib.dump(le,    'model/label_encoder.pkl')
print("✅ Model saved successfully!")