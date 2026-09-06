# Objective 6 — Prevention Engine

This adds a 6th objective on top of the existing 5, without changing how
any of them already work: **actually stopping** the suspicious activity
once it's been detected, not just alerting on it.

Nothing in the original `/alerts`, `/predict`, `/users`, `/timeline`,
`/report-summary`, `/behavior`, or the `/api/*` chart routes was changed.
The only touch to existing code is that `/alerts-verified` and
`/predict-verified` (Objective 5's routes) now also call the prevention
engine after they compute a final severity — that's the "Threat →
Prevention trigger."

## What was fixed from Objective 4

Alerts are now actually **sorted** by severity (High → Medium → Low) in
`Alerts.jsx`, not just color-coded. Previously severity was labeled but
alerts rendered in raw CSV order.

## Architecture

```
modules/db.py                → MongoDB connection, with automatic
                                fallback to a local JSON file if no
                                MongoDB server is reachable
modules/prevention_engine.py → block/unblock logic, status model,
                                file-transfer prevention hook
modules/notifier.py          → admin email notifications (real SMTP if
                                configured, simulated/logged otherwise)
```

### Status model

| Threat level | Status        | Meaning                                  |
|--------------|---------------|-------------------------------------------|
| high         | 🔴 blocked     | user blocked, action/transfer stopped     |
| medium       | 🟡 restricted  | flagged, limited, not fully blocked       |
| low / normal | 🟢 normal      | no action                                  |

### MongoDB (optional)

The project runs with **zero setup** — if no MongoDB server is found at
`MONGO_URI` (default `mongodb://localhost:27017/`), it automatically
falls back to a JSON file at `data/prevention_store.json` that behaves
the same way. To use real MongoDB (e.g. MongoDB Atlas), just set:

```bash
export MONGO_URI="mongodb+srv://<user>:<pass>@<cluster>/"
export MONGO_DB_NAME="threatguard"
```

No code changes needed — `modules/db.py` picks it up automatically on
the next run.

### Email notifications (optional)

By default, admin notifications are printed to the console and stored in
an in-memory log (visible at `GET /prevention/notifications`). To send
real emails, set:

```bash
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASS="your-app-password"
export ADMIN_EMAIL="admin@yourcompany.com"
```

## New API endpoints

| Method | Endpoint                          | Purpose                                   |
|--------|------------------------------------|--------------------------------------------|
| POST   | `/prevention/block`               | Manually block/restrict a user             |
| POST   | `/prevention/unblock`             | Unblock a user after verification          |
| GET    | `/prevention/status/<user_id>`    | Current status for one user                |
| GET    | `/prevention/blocked-users`       | Every user with a non-default status       |
| GET    | `/prevention/logs`                | Full prevention action log                 |
| POST   | `/prevention/check-transfer`      | Check/block a specific file transfer       |
| GET    | `/prevention/notifications`       | Admin notification history                 |

### Example: block a user

```bash
curl -X POST http://localhost:5000/prevention/block \
  -H "Content-Type: application/json" \
  -d '{"user_id":"U045","reason":"Mass download detected","threat_level":"high"}'
```

### Example: check a file transfer

```bash
curl -X POST http://localhost:5000/prevention/check-transfer \
  -H "Content-Type: application/json" \
  -d '{"user_id":"U045","file_name":"customer_db.csv","method":"usb","threat_level":"high"}'
```

Supported `method` values are just labels recorded for the log — `usb`,
`email`, `cloud_upload`, `network_share`, `ftp`, or any custom string you
pass. The blocking decision is driven by `threat_level`, so any transfer
method is supported without code changes.

## Frontend

A new **🛑 Prevention** page (`/prevention`) gives admins:

- Live counts of blocked/restricted users
- A "Run Scan" button that pushes current alerts through ML + the
  Objective 5 verification layer, auto-blocking/restricting as needed
- Manual block/unblock controls
- A file-transfer simulator to test the blocking logic directly
- Full prevention log and admin notification history

The **Alerts** page now also shows a 🛑 *Action Prevented* or 🟡 *User
Restricted* tag next to any alert whose user has already been actioned.

## Idempotency note

`evaluate_and_prevent()` only writes a new log entry when a user's status
actually changes. This means re-running `/alerts-verified` (e.g. a page
refresh) won't spam the log with duplicate entries for the same
detection — it only logs on a genuine state change (first detection, or
an escalation from restricted to blocked).
