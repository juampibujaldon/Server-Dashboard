"""Paquete que agrupa patrones de diseño usados por la aplicación."""

from .singleton import SingletonMeta
from .metrics import (
    MetricBuilder,
    MetricPrototype,
    MetricPrototypeRegistry,
    MetricsObservable,
    MetricObserver,
    CriticalMetricObserver,
    get_metrics_observable,
    get_metric_registry,
    MetricFactory,
)

__all__ = [
    "SingletonMeta",
    "MetricBuilder",
    "MetricPrototype",
    "MetricPrototypeRegistry",
    "MetricsObservable",
    "MetricObserver",
    "CriticalMetricObserver",
    "get_metrics_observable",
    "get_metric_registry",
    "MetricFactory",
]
