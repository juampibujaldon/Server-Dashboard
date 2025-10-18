from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from statistics import mean
from typing import Dict, Iterable, List, Optional

from bson import ObjectId

from app.mapping import MetricMapper
from app.models.metric import Metric
from app.repositories.metrics_repo import MetricsRepository


@dataclass(frozen=True)
class MetricPoint:
    captured_at: Optional[datetime]
    cpu_usage: float
    ram_usage: float
    disk_space: float
    temperature: float
    metric_id: Optional[str] = None


def _extract_timestamp(metric_id: Optional[str]) -> Optional[datetime]:
    if not metric_id:
        return None
    try:
        return ObjectId(metric_id).generation_time.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _build_metric_point(metric: Metric) -> MetricPoint:
    timestamp = _extract_timestamp(metric.id)
    return MetricPoint(
        captured_at=timestamp,
        cpu_usage=metric.cpu_usage,
        ram_usage=metric.ram_usage,
        disk_space=metric.disk_space,
        temperature=metric.temperature,
        metric_id=metric.id,
    )


def _status_bucket(value: float, warning_threshold: float, critical_threshold: float) -> str:
    if value >= critical_threshold:
        return "critical"
    if value >= warning_threshold:
        return "warning"
    return "ok"


def _merge_status(statuses: Iterable[str]) -> str:
    has_critical = False
    has_warning = False
    for status in statuses:
        if status == "critical":
            has_critical = True
        elif status == "warning":
            has_warning = True
    if has_critical:
        return "critical"
    if has_warning:
        return "warning"
    return "ok"


def _calculate_server_status(point: MetricPoint) -> str:
    status_rules = {
        "cpu_usage": (75.0, 90.0),
        "ram_usage": (75.0, 90.0),
        "disk_space": (80.0, 95.0),
        "temperature": (70.0, 85.0),
    }

    statuses = []
    for field, (warning_threshold, critical_threshold) in status_rules.items():
        value = getattr(point, field)
        statuses.append(_status_bucket(value, warning_threshold, critical_threshold))
    return _merge_status(statuses)


def _average(values: Iterable[float]) -> Optional[float]:
    data = list(values)
    if not data:
        return None
    return round(mean(data), 2)


def _serialize_point(point: MetricPoint) -> Dict[str, Optional[float]]:
    return {
        "capturedAt": point.captured_at.isoformat() if point.captured_at else None,
        "cpu": round(point.cpu_usage, 2),
        "ram": round(point.ram_usage, 2),
        "disk": round(point.disk_space, 2),
        "temperature": round(point.temperature, 2),
        "metricId": point.metric_id,
    }


def _serialize_averages(avg: Dict[str, Optional[float]]) -> Dict[str, Optional[float]]:
    return {key: (round(value, 2) if value is not None else None) for key, value in avg.items()}


def get_dashboard_summary(limit_per_server: int = 10) -> Dict[str, object]:
    documents = MetricsRepository.list_all()
    metrics = [MetricMapper.from_document(doc) for doc in documents]

    total_metrics = len(metrics)
    if total_metrics == 0:
        return {
            "summary": {
                "totalServers": 0,
                "totalMetrics": 0,
                "avgCpu": None,
                "avgRam": None,
                "avgDisk": None,
                "avgTemperature": None,
            },
            "servers": [],
            "statusCounts": {"ok": 0, "warning": 0, "critical": 0},
        }

    points_by_server: Dict[str, List[MetricPoint]] = defaultdict(list)
    for metric in metrics:
        points_by_server[metric.server_id].append(_build_metric_point(metric))

    overall_points: List[MetricPoint] = []
    servers_payload: List[Dict[str, object]] = []
    status_counter = {"ok": 0, "warning": 0, "critical": 0}

    for server_id, points in points_by_server.items():
        points_sorted = sorted(
            points, key=lambda p: p.captured_at or datetime.min.replace(tzinfo=timezone.utc)
        )
        overall_points.extend(points_sorted)

        latest_point = points_sorted[-1]
        status = _calculate_server_status(latest_point)
        status_counter[status] += 1

        averages = {
            "cpu": _average(point.cpu_usage for point in points_sorted),
            "ram": _average(point.ram_usage for point in points_sorted),
            "disk": _average(point.disk_space for point in points_sorted),
            "temperature": _average(point.temperature for point in points_sorted),
        }

        trend_points = points_sorted[-limit_per_server:]

        servers_payload.append(
            {
                "serverId": server_id,
                "status": status,
                "latest": _serialize_point(latest_point),
                "averages": _serialize_averages(averages),
                "trend": [_serialize_point(point) for point in trend_points],
            }
        )

    overall_averages = {
        "avgCpu": _average(point.cpu_usage for point in overall_points),
        "avgRam": _average(point.ram_usage for point in overall_points),
        "avgDisk": _average(point.disk_space for point in overall_points),
        "avgTemperature": _average(point.temperature for point in overall_points),
    }

    return {
        "summary": {
            "totalServers": len(points_by_server),
            "totalMetrics": total_metrics,
            **_serialize_averages(overall_averages),
        },
        "servers": sorted(servers_payload, key=lambda s: s["serverId"]),
        "statusCounts": status_counter,
    }
