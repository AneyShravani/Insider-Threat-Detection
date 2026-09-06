# Intelligent Prioritization and Escalation of Insider Threat Alerts Dataset

## Overview
This dataset supports research on intelligent prioritization and escalation of insider threat alerts using machine learning and behavioral analytics. The dataset contains realistic scenarios for training and evaluating models that detect, prioritize, and escalate insider threat alerts.

## Dataset Structure

### 1. User Behavior Analytics (UEBA) Data
- **File**: `ueba_data.csv`
- **Description**: User activity patterns, login behaviors, file access patterns, and application usage
- **Features**: User ID, timestamp, activity type, resource accessed, location, device info, risk score

### 2. Network Security Logs
- **File**: `network_logs.csv`
- **Description**: Network traffic patterns, connection logs, and security events
- **Features**: Source IP, destination IP, port, protocol, timestamp, event type, severity

### 3. Privileged Access Management (PAM) Data
- **File**: `pam_data.csv`
- **Description**: Privileged account activities, elevated access events, and administrative actions
- **Features**: User ID, account type, access level, action performed, timestamp, target system

### 4. Data Loss Prevention (DLP) Events
- **File**: `dlp_events.csv`
- **Description**: Data exfiltration attempts, sensitive data access, and policy violations
- **Features**: User ID, data type, action, file size, destination, timestamp, risk level

### 5. Insider Threat Scenarios
- **File**: `insider_threat_scenarios.csv`
- **Description**: Labeled insider threat incidents with severity levels and escalation paths
- **Features**: Scenario ID, threat type, severity, detection time, escalation path, outcome

### 6. Malware and Ransomware Indicators
- **File**: `malware_indicators.csv`
- **Description**: File behavior patterns, system changes, and suspicious activities
- **Features**: File hash, behavior type, system impact, detection method, timestamp

## Usage Instructions

1. **Data Loading**: Use the provided Python scripts to load and preprocess the data
2. **Feature Engineering**: Extract behavioral patterns and risk indicators
3. **Model Training**: Train DNN and RNN models for alert prioritization
4. **Evaluation**: Use the labeled scenarios to evaluate detection accuracy

## Research Applications

- **Alert Prioritization**: Rank security alerts based on severity and likelihood
- **Behavioral Analytics**: Identify anomalous user behavior patterns
- **Threat Detection**: Detect malware, ransomware, and insider threats
- **Escalation Automation**: Automate alert escalation based on risk scores

## Citation
If you use this dataset in your research, please cite:
```
Intelligent Prioritization and Escalation of Insider Threat Alerts Using Machine Learning and Behavioural Analytics
```

## License
This dataset is provided for academic research purposes only.
