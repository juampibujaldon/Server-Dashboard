from typing import Dict, List, Any, Optional
from bson import ObjectId
from app.db import db_manager
from app.models.server import Server
from dataclasses import asdict

def _col():
    return db_manager.get_db().servers

def create_server(server: Server) -> str:
    res = _col().insert_one(asdict(server))
    return str(res.inserted_id)

def get_server_by_id(server_id: str) -> Optional[Dict[str, Any]]:
    return _col().find_one({"_id": ObjectId(server_id)})

def list_servers() -> List[Dict[str, Any]]:
    return list(_col().find({}))

def update_server(server_id: str, updates: Dict[str, Any]) -> int:
    res = _col().update_one({"_id": ObjectId(server_id)}, {"$set": updates})
    return res.modified_count

def delete_server(server_id: str) -> int:
    res = _col().delete_one({"_id": ObjectId(server_id)})
    return res.deleted_count