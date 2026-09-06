"""
Objective 6 — Admin email notifications for prevention actions.

If SMTP_HOST / SMTP_USER / SMTP_PASS are set as environment variables, a
real email is sent to ADMIN_EMAIL. If they're not configured (the default,
so the project runs without any setup), the notification is printed to the
console and stored in an in-memory log that the /prevention/notifications
endpoint exposes — so the "notify the admin" behavior is fully visible and
testable even without a real mail server.
"""

import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@threatguard.local")

_notification_log = []


def send_admin_alert(subject, body):
    entry = {
        "subject": subject,
        "body": body,
        "to": ADMIN_EMAIL,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    if not (SMTP_HOST and SMTP_USER and SMTP_PASS):
        entry["sent"] = False
        entry["simulated"] = True
        _notification_log.append(entry)
        print(f"[EMAIL SIMULATED] To: {ADMIN_EMAIL} | Subject: {subject}\n{body}\n")
        return entry

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = ADMIN_EMAIL
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [ADMIN_EMAIL], msg.as_string())
        entry["sent"] = True
        entry["simulated"] = False
    except Exception as e:
        entry["sent"] = False
        entry["error"] = str(e)
        print(f"[EMAIL ERROR] {e}")

    _notification_log.append(entry)
    return entry


def get_notification_log():
    return list(reversed(_notification_log))
