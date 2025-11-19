from datetime import datetime
from typing import Any, Dict, List
from zoneinfo import ZoneInfo

from app.mapping import MetricMapper
from app.models.metric import Metric
from app.repositories.metrics_repo import MetricsRepository as Repo

ZONA_TZ = ZoneInfo("America/Argentina/Buenos_Aires")
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

NUMERIC_FIELDS = ("cpu_usage", "ram_usage", "disk_space", "temperature")
PERCENTAGE_FIELDS = ("cpu_usage", "ram_usage", "disk_space")
UPDATE_ALLOWED_FIELDS = {"server_id", *NUMERIC_FIELDS, "sent_at"}


def save_metric(payload: Dict[str, Any]) -> str:
    metric = _build_metric_from_payload(payload)
    metric.sent_at = datetime.now(ZONA_TZ).strftime(DATETIME_FORMAT)
    doc = MetricMapper.to_document(metric)
    metric_id = Repo.insert(doc)

    return metric_id


def replace_metric(metric_id: str, payload: Dict[str, Any]) -> int:
    metric = _build_metric_from_payload(payload)
    metric.sent_at = datetime.now(ZONA_TZ).strftime(DATETIME_FORMAT)
    doc = MetricMapper.to_document(metric)
    return Repo.update_by_id(metric_id, doc)


def find_metrics_by_server(server_id: str) -> List[Dict[str, Any]]:
    return Repo.list_by_server(server_id)


def find_all_metrics() -> List[Dict[str, Any]]:
    return Repo.list_all()


def update_metric_by_id(metric_id: str, updates: Dict[str, Any]) -> int:
    normalized = _normalize_updates(**updates)
    return Repo.update_by_id(metric_id, normalized)


def delete_metric_by_id(metric_id: str) -> int:
    return Repo.delete_by_id(metric_id)


def delete_metrics_by_server(server_id: str) -> int:
    return Repo.delete_by_server(server_id)


def _build_metric_from_payload(payload: Dict[str, Any]) -> Metric:
    return Metric(
        server_id=str(payload["server_id"]),
        cpu_usage=float(payload["cpu_usage"]),
        ram_usage=float(payload["ram_usage"]),
        disk_space=float(payload["disk_space"]),
        temperature=float(payload["temperature"]),
        sent_at=payload.get("sent_at"),
        id=payload.get("id"),
    )


def _normalize_updates(**updates: Any) -> Dict[str, Any]:
    if not updates:
        raise ValueError("No hay campos para actualizar")

    normalized: Dict[str, Any] = {}
    for field, value in updates.items():
        if field not in UPDATE_ALLOWED_FIELDS:
            raise ValueError(f"Campo no permitido para actualizar: {field}")

        if field in NUMERIC_FIELDS:
            try:
                coerced = float(value)
            except Exception as exc:
                raise ValueError(f"El campo {field} debe ser numérico") from exc
            if field in PERCENTAGE_FIELDS and not 0 <= coerced <= 100:
                raise ValueError(f"El campo {field} debe estar entre 0 y 100")
            normalized[field] = coerced
            continue

        if field == "server_id":
            if not value:
                raise ValueError("El campo server_id no puede estar vacío")
            normalized[field] = str(value)
            continue

        # sent_at u otros campos string
        normalized[field] = value
    return normalized
