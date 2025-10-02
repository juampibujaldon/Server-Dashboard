"""Conversión entre objetos Metric y los diccionarios usados por Mongo."""

from dataclasses import asdict
from typing import Dict

from app.models.metric import Metric


class MetricMapper:
    """Aplica el patrón Mapping para desacoplar dominio de la capa de persistencia."""

    @staticmethod
    def to_document(metric: Metric) -> Dict:
        doc = asdict(metric)
        if doc.get("id") is None:
            doc.pop("id")
        return doc

    @staticmethod
    def from_document(document: Dict) -> Metric:
        data = document.copy()
        if "_id" in data:
            data["id"] = str(data.pop("_id"))
        return Metric(**data)
