"""Patrones relacionados con el ciclo de vida de las métricas."""

from typing import Dict, List, Protocol

from app.models.metric import Metric
from app.models.alert import Alert


class MetricObserver(Protocol):
    def on_metric_saved(self, metric: Metric) -> None:
        ...


class MetricsObservable:
    """Notifica a observadores cuando se persiste una métrica."""

    def __init__(self):
        self._observers: List[MetricObserver] = []

    def subscribe(self, observer: MetricObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: MetricObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, metric: Metric) -> None:
        for observer in list(self._observers):
            observer.on_metric_saved(metric)


class CriticalMetricObserver(MetricObserver):
    """Genera alertas simples si una métrica supera umbrales críticos."""

    def __init__(self, thresholds: Dict[str, float] | None = None):
        self.thresholds = thresholds or {
            "cpu_usage": 90.0,
            "ram_usage": 95.0,
            "disk_space": 90.0,
            "temperature": 80.0,
        }

    def on_metric_saved(self, metric: Metric) -> None:
        breaches = [
            (name, getattr(metric, name))
            for name, limit in self.thresholds.items()
            if getattr(metric, name) > limit
        ]
        if not breaches:
            return

        severity = ", ".join(f"{name}={value:.1f}" for name, value in breaches)
        alert = Alert(
            server_id=metric.server_id,
            metric_type="critical_metric",
            threshold=max(value for _, value in breaches),
            condition=severity,
        )
        try:
            from app.services import alert_services
            alert_services.create_alert(alert)
        except Exception:
            # Preferimos no romper el flujo si falla el guardado del alerta
            pass


# Registro inicial por módulo -------------------------------------------------

_metrics_observable = MetricsObservable()
_metrics_observable.subscribe(CriticalMetricObserver())


def get_metrics_observable() -> MetricsObservable:
    return _metrics_observable
