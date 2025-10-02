from flask import jsonify, request
from flask.views import MethodView

from app.services import metric_services
from app.utils.serialization import serialize_many
from app.utils.validation import validate_metric_payload


class MetricsResource(MethodView):

    def post(self):
        payload = request.get_json(silent=True) or {}
        if not payload:
            return jsonify({"error": "Cuerpo de la petición inválido"}), 400

        ok, error_message = validate_metric_payload(payload)
        if not ok:
            return jsonify({"error": error_message}), 400

        try:
            metric_services.save_metric(payload)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception:
            # No exponemos información sensible al cliente
            return (
                jsonify({"error": "Ocurrió un error en el servidor"}),
                500,
            )

        return jsonify({"message": "Métrica añadida correctamente"}), 201


class MetricsByServerResource(MethodView):

    def get(self, server_id: str):
        metrics = metric_services.find_metrics_by_server(server_id)
        return jsonify(serialize_many(metrics)), 200

__all__ = ["MetricsResource", "MetricsByServerResource"]
