from datetime import datetime
from typing import Any, Dict, List
from zoneinfo import ZoneInfo

from app.mapping import MetricMapper
from app.patterns import MetricBuilder, MetricFactory, get_metrics_observable
from app.repositories.metrics_repo import MetricsRepository as Repo

ARGENTINA_TZ = ZoneInfo("America/Argentina/Buenos_Aires")
ARGENTINA_DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"


def save_metric(payload: Dict[str, Any]) -> str:
    metric = MetricFactory.from_payload(payload)
    metric.sent_at = datetime.now(ARGENTINA_TZ).strftime(ARGENTINA_DATETIME_FORMAT)
    doc = MetricMapper.to_document(metric)
    metric_id = Repo.insert(doc)

    metric_with_id = MetricBuilder(metric.to_dict()).with_id(metric_id).build()
    get_metrics_observable().notify(metric_with_id)

    return metric_id


def find_metrics_by_server(server_id: str) -> List[Dict[str, Any]]:
    return Repo.list_by_server(server_id)


def find_all_metrics() -> List[Dict[str, Any]]:
    return Repo.list_all()


def update_metric_by_id(metric_id: str, updates: Dict[str, Any]) -> int:
    return Repo.update_by_id(metric_id, updates)


def delete_metric_by_id(metric_id: str) -> int:
    return Repo.delete_by_id(metric_id)


def delete_metrics_by_server(server_id: str) -> int:
    return Repo.delete_by_server(server_id)
