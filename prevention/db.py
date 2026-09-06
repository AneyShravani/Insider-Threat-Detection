"""
prevention/db.py
-----------------
MongoDB connection layer for the Prevention Engine.

Collections:
  - blocked_users     : current block/suspend status per user
  - prevention_logs   : full audit trail of every prevention decision/action

If MongoDB is not reachable (e.g. not installed / not running / no URI
configured), this module falls back to a simple in-memory store so the
rest of the team can still run and demo the API without a live DB.
Set MONGO_URI (and optionally MONGO_DB_NAME) in your environment / .env
to point at a real MongoDB instance (local or Atlas).
"""

import os
from datetime import datetime, timezone

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "insider_threat_db")

USING_MONGO = False
blocked_users_col = None
prevention_logs_col = None

try:
    from pymongo import MongoClient, ASCENDING, DESCENDING

    _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    _client.admin.command("ping")  # fail fast if Mongo isn't reachable

    _db = _client[DB_NAME]
    blocked_users_col = _db["blocked_users"]
    prevention_logs_col = _db["prevention_logs"]

    blocked_users_col.create_index("user_id", unique=True)
    prevention_logs_col.create_index([("timestamp", DESCENDING)])
    prevention_logs_col.create_index("user_id")

    USING_MONGO = True
    print(f"[prevention] Connected to MongoDB ({MONGO_URI}, db='{DB_NAME}')")
except Exception as exc:
    print(
        f"[prevention] WARNING: could not connect to MongoDB ({exc}). "
        "Falling back to in-memory storage (data will NOT persist between restarts). "
        "Set MONGO_URI to enable real persistence."
    )


# ---------------------------------------------------------------------------
# In-memory fallback store (mimics the tiny subset of pymongo we use)
# ---------------------------------------------------------------------------
_mem_blocked = {}   # user_id -> doc
_mem_logs = []       # list of docs, newest first


def now_iso():
    return datetime.now(timezone.utc).isoformat()


# ---------------------- blocked_users helpers ----------------------

def get_blocked_user(user_id):
    if USING_MONGO:
        return blocked_users_col.find_one({"user_id": user_id}, {"_id": 0})
    return _mem_blocked.get(user_id)


def is_user_blocked(user_id):
    return get_blocked_user(user_id) is not None


def upsert_blocked_user(doc):
    """doc must contain 'user_id'. Overwrites any existing block record."""
    if USING_MONGO:
        blocked_users_col.update_one(
            {"user_id": doc["user_id"]}, {"$set": doc}, upsert=True
        )
    else:
        _mem_blocked[doc["user_id"]] = doc
    return doc


def remove_blocked_user(user_id):
    existed = is_user_blocked(user_id)
    if USING_MONGO:
        blocked_users_col.delete_one({"user_id": user_id})
    else:
        _mem_blocked.pop(user_id, None)
    return existed


def list_blocked_users():
    if USING_MONGO:
        return list(blocked_users_col.find({}, {"_id": 0}))
    return list(_mem_blocked.values())


# ---------------------- prevention_logs helpers ----------------------

def insert_log(doc):
    doc.setdefault("timestamp", now_iso())
    if USING_MONGO:
        prevention_logs_col.insert_one(dict(doc))
    else:
        _mem_logs.insert(0, doc)
    return doc


def get_logs(user_id=None, threat_level=None, limit=100):
    query = {}
    if user_id:
        query["user_id"] = user_id
    if threat_level:
        query["threat_level"] = threat_level

    if USING_MONGO:
        cursor = (
            prevention_logs_col.find(query, {"_id": 0})
            .sort("timestamp", -1)
            .limit(limit)
        )
        return list(cursor)

    results = [
        log
        for log in _mem_logs
        if (not user_id or log.get("user_id") == user_id)
        and (not threat_level or log.get("threat_level") == threat_level)
    ]
    return results[:limit]