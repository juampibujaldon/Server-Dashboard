"""Patrones relacionados con el ciclo de vida de las métricas."""

from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List, Protocol

from app.models.metric import Metric
from app.patterns.singleton import SingletonMeta
from app.services import alert_services
from app.models.alert import Alert


# --- Builder -----------------------------------------------------------------


class MetricBuilder:
    """Construye objetos Metric garantizando validaciones básicas."""

    def __init__(self, base: Dict | None = None):
        self._data: Dict = base.copy() if base else {}

    def with_server(self, server_id: str) -> "MetricBuilder":
        self._data["serverId"] = server_id
        return self

    def with_cpu_usage(self, cpu: float) -> "MetricBuilder":
        self._data["cpu_usage"] = float(cpu)
        return self

    def with_ram_usage(self, ram: float) -> "MetricBuilder":
        self._data["ram_usage"] = float(ram)
        return self

    def with_disk_space(self, disk: float) -> "MetricBuilder":
        self._data["disk_space"] = float(disk)
        return self

    def with_temperature(self, temp: float) -> "MetricBuilder":
        self._data["temperature"] = float(temp)
        return self

    def with_id(self, metric_id: str | None) -> "MetricBuilder":
        if metric_id is not None:
            self._data["id"] = metric_id
        return self

    def build(self) -> Metric:
        required = ("serverId", "cpu_usage", "ram_usage", "disk_space", "temperature")
        missing = [field for field in required if field not in self._data]
        if missing:
            raise ValueError(f"Faltan campos obligatorios en MetricBuilder: {', '.join(missing)}")
        return Metric(**self._data)

    @classmethod
    def from_payload(cls, payload: Dict) -> Metric:
        builder = cls()
        builder.with_server(payload["serverId"])  # type: ignore[index]
        builder.with_cpu_usage(payload["cpu_usage"])
        builder.with_ram_usage(payload["ram_usage"])
        builder.with_disk_space(payload["disk_space"])
        builder.with_temperature(payload["temperature"])
        return builder.build()


# --- Prototype ---------------------------------------------------------------


class MetricPrototype:
    """Permite clonar métricas base y sobreescribir campos puntuales."""

    def __init__(self, template: Metric):
        self._template = template

    def clone(self, **overrides) -> Metric:
        data = asdict(self._template)
        data.update(overrides)
        builder = MetricBuilder(data)
        return builder.build()


class MetricPrototypeRegistry(metaclass=SingletonMeta):
    """Registro centralizado de prototipos de métricas."""

    def __init__(self):
        self._prototypes: Dict[str, MetricPrototype] = {}

    def register(self, name: str, prototype: MetricPrototype) -> None:
        self._prototypes[name] = prototype

    def clone(self, name: str, **overrides) -> Metric:
        prototype = self._prototypes.get(name)
        if not prototype:
            raise KeyError(f"No existe prototipo para {name}")
        return prototype.clone(**overrides)

    def ensure_default(self) -> None:
        if "default" not in self._prototypes:
            base = Metric("unknown", 0.0, 0.0, 0.0, 0.0)
            self.register("default", MetricPrototype(base))


# --- Observer ----------------------------------------------------------------


class MetricObserver(Protocol):
    def on_metric_saved(self, metric: Metric) -> None:
        ...


class MetricsObservable(metaclass=SingletonMeta):
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
            serverId=metric.serverId,
            metric_type="critical_metric",
            threshold=max(value for _, value in breaches),
            condition=severity,
        )
        try:
            alert_services.create_alert(alert)
        except Exception:
            # Preferimos no romper el flujo si falla el guardado del alerta
            pass


# Registro inicial por módulo -------------------------------------------------

_registry = MetricPrototypeRegistry()
_registry.ensure_default()

_metrics_observable = MetricsObservable()
_metrics_observable.subscribe(CriticalMetricObserver())


def get_metrics_observable() -> MetricsObservable:
    return _metrics_observable


def get_metric_registry() -> MetricPrototypeRegistry:
    return _registry


class MetricFactory:
    """Factory Method para crear métricas a partir de distintos orígenes."""

    @staticmethod
    def from_payload(payload: Dict) -> Metric:
        registry = get_metric_registry()
        base_metric = registry.clone("default")
        builder = MetricBuilder(base_metric.to_dict())
        builder.with_server(payload["serverId"])
        builder.with_cpu_usage(payload["cpu_usage"])
        builder.with_ram_usage(payload["ram_usage"])
        builder.with_disk_space(payload["disk_space"])
        builder.with_temperature(payload["temperature"])
        return builder.build()
