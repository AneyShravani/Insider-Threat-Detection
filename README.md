# Insider Threat Detection System

A machine learning-based security system that analyzes user activity and identifies potentially malicious or abnormal behavior. The system combines behavioral analysis, machine learning-based threat detection, risk classification, and automated prevention mechanisms.

## Overview

Insider threats can occur when legitimate users misuse their access to organizational resources. This project analyzes user activity such as login behavior, file access, and restricted-resource interactions to identify suspicious patterns.

The system generates threat alerts and classifies detected activity into **Low, Medium, and High** risk levels. High-risk activity can trigger prevention actions such as blocking users or stopping suspicious file transfers.

## Tech Stack

* **Python**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **Flask**
* **MongoDB**
* **HTML/CSS/JavaScript**
* **Git & GitHub**

## Machine Learning

The project uses machine learning models to analyze behavioral features and classify potentially suspicious activity.

### Data Processing

* Data cleaning and preprocessing
* Feature extraction
* Feature validation
* Behavioral activity analysis
* Training and evaluation of classification models

### Model

A **Random Forest classifier** is used for threat classification.

The model analyzes activity-related features and produces predictions that are used by the alert and risk-scoring system.

## Risk Classification

Detected activity is categorized into three threat levels:

| Risk Level      | Response                                              |
| --------------- | ----------------------------------------------------- |
| 🔴 High         | User blocked and suspicious action/transfer prevented |
| 🟡 Medium       | User restricted and activity flagged                  |
| 🟢 Low / Normal | No preventive action                                  |

## Key Features

### Threat Detection

* Analyzes user activity and behavioral patterns.
* Detects potentially abnormal or unauthorized activity.
* Generates structured security alerts.
* Sorts alerts based on threat severity.

### Risk Scoring

* Classifies detected activity as Low, Medium, or High risk.
* Provides structured information for security investigation.

### Prevention Engine

The system extends detection beyond alert generation by providing automated prevention mechanisms.

* Block or restrict suspicious users.
* Unblock users after verification.
* Track prevention actions.
* Check potentially risky file transfers.
* Maintain prevention logs.
* Generate administrator notifications.

### File Transfer Protection

The system can evaluate file-transfer activity and apply prevention rules based on the detected threat level.

Supported transfer types include:

* USB
* Email
* Cloud Upload
* Network Share
* FTP

### Dashboard

The Flask-based dashboard provides interfaces for:

* Security alerts
* User behavior analysis
* Activity timelines
* Prediction results
* Reports
* Prevention management
* Notifications

## System Architecture

```text
                    User Activity
                         │
                         ▼
                ┌─────────────────┐
                │ Data Processing │
                │ & Feature       │
                │ Engineering     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Machine Learning │
                │ Random Forest   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Risk Assessment │
                │ Low / Medium /  │
                │ High            │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       ┌──────────────┐      ┌───────────────┐
       │    Alerts    │      │  Prevention   │
       │ & Dashboard  │      │    Engine     │
       └──────────────┘      └───────┬───────┘
                                     │
                            ┌────────┴────────┐
                            ▼                 ▼
                       User Action      Notifications
                    Block / Restrict
```

## Backend APIs

The application provides APIs for threat analysis, alerts, user behavior, reporting, and prevention.

### Prevention APIs

| Method | Endpoint                       | Purpose                          |
| ------ | ------------------------------ | -------------------------------- |
| POST   | `/prevention/block`            | Block or restrict a user         |
| POST   | `/prevention/unblock`          | Unblock a user                   |
| GET    | `/prevention/status/<user_id>` | Check user status                |
| GET    | `/prevention/blocked-users`    | View restricted/blocked users    |
| GET    | `/prevention/logs`             | View prevention actions          |
| POST   | `/prevention/check-transfer`   | Evaluate a file transfer         |
| GET    | `/prevention/notifications`    | View administrator notifications |

## Database

MongoDB can be used to store prevention-related information and system state.

The application also supports a local JSON fallback when a MongoDB server is unavailable, allowing the prevention functionality to run without requiring a database server setup.

## Project Structure

```text
Insider-Threat-Detection/
│
├── config/
├── data/
├── frontend/
├── logs/
├── model/
├── modules/
│   ├── db.py
│   ├── prevention_engine.py
│   └── notifier.py
│
├── app.py
├── train_model.py
├── requirements.txt
├── PREVENTION_README.md
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/AneyShravani/Insider-Threat-Detection.git
cd Insider-Threat-Detection
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the model

```bash
python train_model.py
```

### 5. Start the Flask application

```bash
python app.py
```

Open the application in your browser using the local address displayed by Flask.

## Security & Configuration

Sensitive configuration values such as database credentials, SMTP credentials, and other secrets should be provided through environment variables rather than committed to the repository.

The project does not require real credentials for its basic local prevention workflow.

## Future Enhancements

* Deploy the application on AWS.
* Add real-time activity monitoring.
* Improve behavioral anomaly detection.
* Integrate additional machine learning models.
* Add centralized security monitoring.
* Implement containerized deployment using Docker.
* Add CI/CD automation.

## Author

**Shravani Aney**

GitHub: https://github.com/AneyShravani
