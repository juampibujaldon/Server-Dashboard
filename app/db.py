import os
import time
from copy import deepcopy
from urllib.parse import urlparse

from bson import ObjectId
from flask import current_app
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError

from app.patterns import SingletonMeta

try:
    import mongomock
except Exception:
    mongomock = None


class _InsertOneResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class _InsertManyResult:
    def __init__(self, inserted_ids):
        self.inserted_ids = inserted_ids


class _UpdateResult:
    def __init__(self, matched_count: int, modified_count: int):
        self.matched_count = matched_count
        self.modified_count = modified_count


class _DeleteResult:
    def __init__(self, deleted_count: int):
        self.deleted_count = deleted_count


class _InMemoryCollection:
    def __init__(self):
        self._docs = []

    def _ensure_id(self, doc):
        if doc.get("_id") is None:
            doc["_id"] = ObjectId()
        elif not isinstance(doc["_id"], ObjectId):
            doc["_id"] = ObjectId(str(doc["_id"]))

    @staticmethod
    def _matches(doc, query):
        if not query:
            return True
        for key, expected in query.items():
            actual = doc.get(key)
            if key == "_id":
                if isinstance(expected, ObjectId):
                    if actual != expected:
                        return False
                else:
                    if str(actual) != str(expected):
                        return False
            else:
                if actual != expected:
                    return False
        return True

    def insert_one(self, doc):
        new_doc = deepcopy(doc)
        self._ensure_id(new_doc)
        self._docs.append(new_doc)
        return _InsertOneResult(new_doc["_id"])

    def insert_many(self, docs):
        inserted_ids = []
        for doc in docs:
            inserted_ids.append(self.insert_one(doc).inserted_id)
        return _InsertManyResult(inserted_ids)

    def find(self, query=None):
        query = query or {}
        return [deepcopy(doc) for doc in self._docs if self._matches(doc, query)]

    def find_one(self, query=None):
        query = query or {}
        for doc in self._docs:
            if self._matches(doc, query):
                return deepcopy(doc)
        return None

    def update_one(self, query, update):
        query = query or {}
        matched = 0
        modified = 0
        changes = update.get("$set", {}) if isinstance(update, dict) else {}
        for doc in self._docs:
            if self._matches(doc, query):
                matched = 1
                if changes:
                    doc.update(changes)
                    modified = 1
                break
        return _UpdateResult(matched, modified)

    def delete_one(self, query):
        query = query or {}
        for idx, doc in enumerate(self._docs):
            if self._matches(doc, query):
                del self._docs[idx]
                return _DeleteResult(1)
        return _DeleteResult(0)

    def delete_many(self, query):
        query = query or {}
        remaining = []
        deleted = 0
        for doc in self._docs:
            if self._matches(doc, query):
                deleted += 1
            else:
                remaining.append(doc)
        self._docs = remaining
        return _DeleteResult(deleted)

    def count_documents(self, query):
        query = query or {}
        return sum(1 for doc in self._docs if self._matches(doc, query))

    def create_index(self, *_args, **_kwargs):
        return "in_memory_index"


class _InMemoryDatabase:
    def __init__(self):
        self._collections = {}

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        return self._collections.setdefault(name, _InMemoryCollection())

    def __getitem__(self, name):
        return self.__getattr__(name)


class _InMemoryAdmin:
    @staticmethod
    def command(cmd):
        if cmd == "ping":
            return {"ok": 1}
        raise NotImplementedError(cmd)


class InMemoryMongoClient:
    def __init__(self):
        self._databases = {}
        self._admin = _InMemoryAdmin()

    def __getitem__(self, name):
        return self._databases.setdefault(name, _InMemoryDatabase())

    @property
    def admin(self):
        return self._admin

    def close(self):
        self._databases.clear()


class DBManager(metaclass=SingletonMeta):
    def __init__(self):
        self.client = None

    def init_app(self, app):
        mongo_uri = app.config.get("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI is not configured in the Flask app.")

        env_name = os.getenv("BACKEND_ENV", "development").lower()

        if env_name == "testing":
            if mongomock is not None:
                self.client = mongomock.MongoClient()
            else:
                self.client = InMemoryMongoClient()
        else:
            max_attempts = int(os.getenv("MONGO_CONNECT_MAX_ATTEMPTS", "10"))
            initial_delay_seconds = float(os.getenv("MONGO_CONNECT_INITIAL_DELAY", "0.5"))
            attempt = 0
            delay = initial_delay_seconds

            while attempt < max_attempts:
                attempt += 1
                try:
                    self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
                    self.client.admin.command("ping")
                    print(f"Connected to MongoDB on attempt {attempt}")
                    break
                except (ServerSelectionTimeoutError, ConfigurationError) as exc:
                    print(f"Attempt {attempt}/{max_attempts} to connect to MongoDB failed: {exc}")
                    if attempt >= max_attempts:
                        raise
                    time.sleep(delay)
                    delay = min(delay * 2, 5.0)

        @app.teardown_appcontext
        def close_db(_exception):
            pass

    def get_db(self):
        if not self.client:
            raise RuntimeError("Database has not been initialised. Call init_app first.")

        cfg_uri = current_app.config.get("MONGO_URI", "")
        db_name = None
        try:
            parsed = urlparse(cfg_uri)
            path = (parsed.path or "/").lstrip("/")
            db_name = path.split("?")[0] or None
        except Exception:
            db_name = None
        if not db_name:
            db_name = "test_db" if os.getenv("BACKEND_ENV", "development").lower() == "testing" else "app_db"

        db = self.client[db_name]
        try:
            db.metrics.create_index("serverId")
            db.alerts.create_index("serverId")
        except Exception:
            pass
        return db


db_manager = DBManager()
