from typing import Dict, List, Any
from app.repositories.metrics_repo import MetricsRepository as Repo


def save_metric(payload: Dict[str, Any]) -> str:
    return Repo.insert(payload)


def find_metrics_by_server(server_id: str) -> List[Dict[str, Any]]:
    return Repo.list_by_server(server_id)


def update_metric_by_id(metric_id: str, updates: Dict[str, Any]) -> int:
    return Repo.update_by_id(metric_id, updates)


def delete_metric_by_id(metric_id: str) -> int:
    return Repo.delete_by_id(metric_id)


def delete_metrics_by_server(server_id: str) -> int:
    return Repo.delete_by_server(server_id)
