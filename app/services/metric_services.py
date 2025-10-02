from typing import Any, Dict, List

from app.mapping import MetricMapper
from app.patterns import MetricBuilder, MetricFactory, get_metrics_observable
from app.repositories.metrics_repo import MetricsRepository as Repo


def save_metric(payload: Dict[str, Any]) -> str:
    metric = MetricFactory.from_payload(payload)
    doc = MetricMapper.to_document(metric)
    metric_id = Repo.insert(doc)

    metric_with_id = MetricBuilder(metric.to_dict()).with_id(metric_id).build()
    get_metrics_observable().notify(metric_with_id)

    return metric_id


def find_metrics_by_server(server_id: str) -> List[Dict[str, Any]]:
    return Repo.list_by_server(server_id)


def update_metric_by_id(metric_id: str, updates: Dict[str, Any]) -> int:
    return Repo.update_by_id(metric_id, updates)


def delete_metric_by_id(metric_id: str) -> int:
    return Repo.delete_by_id(metric_id)


def delete_metrics_by_server(server_id: str) -> int:
    return Repo.delete_by_server(server_id)
