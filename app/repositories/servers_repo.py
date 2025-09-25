from typing import Dict, Any, List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from app.db import db_manager


class ServersRepository:
    @staticmethod
    def _col():
        return db_manager.get_db().servers

    @classmethod
    def insert(cls, server_doc: Dict[str, Any]) -> str:
        res = cls._col().insert_one(server_doc)
        return str(res.inserted_id)

    @classmethod
    def get_by_id(cls, server_id: str) -> Optional[Dict[str, Any]]:
        try:
            oid = ObjectId(server_id)
        except (InvalidId, TypeError):
            raise ValueError("ID de servidor inválido")
        return cls._col().find_one({"_id": oid})

    @classmethod
    def list_all(cls) -> List[Dict[str, Any]]:
        return list(cls._col().find({}))

    @classmethod
    def update(cls, server_id: str, updates: Dict[str, Any]) -> int:
        try:
            oid = ObjectId(server_id)
        except (InvalidId, TypeError):
            raise ValueError("ID de servidor inválido")
        res = cls._col().update_one({"_id": oid}, {"$set": updates})
        return res.modified_count

    @classmethod
    def delete(cls, server_id: str) -> int:
        try:
            oid = ObjectId(server_id)
        except (InvalidId, TypeError):
            raise ValueError("ID de servidor inválido")
        res = cls._col().delete_one({"_id": oid})
        return res.deleted_count

