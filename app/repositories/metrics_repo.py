from typing import Dict, Any, List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from app.db import db_manager


class MetricsRepository:
    @staticmethod
    def _col():
        return db_manager.get_db().metrics

    @classmethod
    def insert(cls, metric: Dict[str, Any]) -> str:
        res = cls._col().insert_one(metric)
        return str(res.inserted_id)

    @classmethod
    def list_by_server(cls, server_id: str) -> List[Dict[str, Any]]:
        return list(cls._col().find({"serverId": server_id}))

    @classmethod
    def update_by_id(cls, metric_id: str, updates: Dict[str, Any]) -> int:
        try:
            oid = ObjectId(metric_id)
        except (InvalidId, TypeError):
            raise ValueError("ID de métrica inválido")
        res = cls._col().update_one({"_id": oid}, {"$set": updates})
        return res.modified_count

    @classmethod
    def delete_by_id(cls, metric_id: str) -> int:
        try:
            oid = ObjectId(metric_id)
        except (InvalidId, TypeError):
            raise ValueError("ID de métrica inválido")
        res = cls._col().delete_one({"_id": oid})
        return res.deleted_count

    @classmethod
    def delete_by_server(cls, server_id: str) -> int:
        res = cls._col().delete_many({"serverId": server_id})
        return res.deleted_count

