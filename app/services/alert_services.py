from typing import Dict, List, Any, Optional
from dataclasses import asdict
from app.models.alert import Alert
from app.repositories.alerts_repo import AlertsRepository as Repo


def create_alert(alert: Alert) -> str:
    return Repo.insert(asdict(alert))


def get_alert_by_id(alert_id: str) -> Optional[Dict[str, Any]]:
    return Repo.get_by_id(alert_id)


def list_alerts_by_server(server_id: str) -> List[Dict[str, Any]]:
    return Repo.list_by_server(server_id)


def update_alert(alert_id: str, updates: Dict[str, Any]) -> int:
    return Repo.update(alert_id, updates)


def delete_alert(alert_id: str) -> int:
    return Repo.delete(alert_id)
