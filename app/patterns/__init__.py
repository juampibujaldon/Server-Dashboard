"""Paquete que agrupa patrones de diseño usados por la aplicación."""

from .metrics import (
    MetricsObservable,
    MetricObserver,
    CriticalMetricObserver,
    get_metrics_observable,
)

__all__ = [
    "MetricsObservable",
    "MetricObserver",
    "CriticalMetricObserver",
    "get_metrics_observable",
]
