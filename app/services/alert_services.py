from typing import Dict, List, Any, Optional
from bson import ObjectId
from dataclasses import asdict
from app.db import db_manager
from app.models.alert import Alert

def _col():
    return db_manager.get_db().alerts

def create_alert(alert: Alert) -> str:
    res = _col().insert_one(asdict(alert))
    return str(res.inserted_id)

def get_alert_by_id(alert_id: str) -> Optional[Dict[str, Any]]:
    return _col().find_one({"_id": ObjectId(alert_id)})

def list_alerts_by_server(server_id: str) -> List[Dict[str, Any]]:
    return list(_col().find({"serverId": server_id}))

def update_alert(alert_id: str, updates: Dict[str, Any]) -> int:
    res = _col().update_one({"_id": ObjectId(alert_id)}, {"$set": updates})
    return res.modified_count

def delete_alert(alert_id: str) -> int:
    res = _col().delete_one({"_id": ObjectId(alert_id)})
    return res.deleted_count