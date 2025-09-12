from typing import Dict, List, Any
from bson import ObjectId
from app.db import db_manager

def _col():
    return db_manager.get_db().metrics

def save_metric(payload: Dict[str, Any]) -> str:
    res = _col().insert_one(payload)
    return str(res.inserted_id)

def find_metrics_by_server(server_id: str) -> List[Dict[str, Any]]:
    return list(_col().find({"serverId": server_id}))

def update_metric_by_id(metric_id: str, updates: Dict[str, Any]) -> int:
    res = _col().update_one({"_id": ObjectId(metric_id)}, {"$set": updates})
    return res.modified_count

def delete_metric_by_id(metric_id: str) -> int:
    res = _col().delete_one({"_id": ObjectId(metric_id)})
    return res.deleted_count

def delete_metrics_by_server(server_id: str) -> int:
    res = _col().delete_many({"serverId": server_id})
    return res.deleted_count