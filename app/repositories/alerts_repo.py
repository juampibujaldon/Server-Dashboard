from typing import Dict, Any, List, Optional
from bson import ObjectId
from bson.errors import InvalidId


class AlertsRepository:
    @staticmethod
    def _col():
        from app.db import db_manager
        return db_manager.get_db().alerts

    @classmethod
    def insert(cls, alert_doc: Dict[str, Any]) -> str:
        res = cls._col().insert_one(alert_doc)
        return str(res.inserted_id)

    @classmethod
    def get_by_id(cls, alert_id: str) -> Optional[Dict[str, Any]]:
        try:
            oid = ObjectId(alert_id)
        except (InvalidId, TypeError):
            raise ValueError("ID de alerta inválido")
        return cls._col().find_one({"_id": oid})

    @classmethod
    def list_by_server(cls, server_id: str) -> List[Dict[str, Any]]:
        return list(cls._col().find({"server_id": server_id}))

    @classmethod
    def update(cls, alert_id: str, updates: Dict[str, Any]) -> int:
        try:
            oid = ObjectId(alert_id)
        except (InvalidId, TypeError):
            raise ValueError("ID de alerta inválido")
        res = cls._col().update_one({"_id": oid}, {"$set": updates})
        return res.modified_count

    @classmethod
    def delete(cls, alert_id: str) -> int:
        try:
            oid = ObjectId(alert_id)
        except (InvalidId, TypeError):
            raise ValueError("ID de alerta inválido")
        res = cls._col().delete_one({"_id": oid})
        return res.deleted_count

