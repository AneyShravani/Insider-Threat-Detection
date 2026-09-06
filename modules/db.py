"""
Objective 6 — Prevention Engine storage layer.

Uses MongoDB when it's available (set MONGO_URI to point at your own
instance / Atlas cluster). If no MongoDB server can be reached, it falls
back automatically to a local JSON file (data/prevention_store.json) that
speaks the same find_one / find / insert_one / update_one interface, so
the rest of the codebase never needs to know which backend is active.

This means the project runs out of the box with zero setup, and upgrades
to real MongoDB the moment MONGO_URI is pointed at a live server.
"""

import os
import json
import threading

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.environ.get("MONGO_DB_NAME", "threatguard")

_lock = threading.Lock()
_USE_MONGO = False
_db = None

try:
    from pymongo import MongoClient
    _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1200)
    _client.admin.command("ping")
    _db = _client[DB_NAME]
    _USE_MONGO = True
    print(f"[Prevention DB] Connected to MongoDB at {MONGO_URI}")
except Exception as e:
    _USE_MONGO = False
    print(f"[Prevention DB] MongoDB not reachable ({e}).")
    print("[Prevention DB] Falling back to local JSON storage at data/prevention_store.json")

_JSON_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "prevention_store.json")
)


def _load_json():
    if not os.path.exists(_JSON_PATH):
        return {"blocked_users": [], "prevention_logs": []}
    with open(_JSON_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"blocked_users": [], "prevention_logs": []}


def _save_json(data):
    os.makedirs(os.path.dirname(_JSON_PATH), exist_ok=True)
    with open(_JSON_PATH, "w") as f:
        json.dump(data, f, indent=2, default=str)


class JsonCollection:
    """Minimal Mongo-collection-shaped interface backed by a JSON file."""

    def __init__(self, name):
        self.name = name
        data = _load_json()
        if self.name not in data:
            data[self.name] = []
            _save_json(data)

    def find_one(self, query):
        data = _load_json()
        for doc in data.get(self.name, []):
            if all(doc.get(k) == v for k, v in query.items()):
                return doc
        return None

    def find(self, query=None):
        data = _load_json()
        docs = data.get(self.name, [])
        if not query:
            return list(docs)
        return [d for d in docs if all(d.get(k) == v for k, v in query.items())]

    def insert_one(self, doc):
        with _lock:
            data = _load_json()
            data.setdefault(self.name, []).append(doc)
            _save_json(data)
        return doc

    def update_one(self, query, update):
        with _lock:
            data = _load_json()
            for doc in data.get(self.name, []):
                if all(doc.get(k) == v for k, v in query.items()):
                    doc.update(update.get("$set", {}))
                    _save_json(data)
                    return doc
            return None

    def delete_one(self, query):
        with _lock:
            data = _load_json()
            docs = data.get(self.name, [])
            for i, doc in enumerate(docs):
                if all(doc.get(k) == v for k, v in query.items()):
                    del docs[i]
                    _save_json(data)
                    return True
            return False


def get_collection(name):
    """Returns a MongoDB collection if connected, otherwise a JSON-backed
    stand-in with the same basic interface."""
    if _USE_MONGO:
        return _db[name]
    return JsonCollection(name)


def using_mongo():
    return _USE_MONGO
