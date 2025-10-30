from flask import jsonify, request
from flask.views import MethodView

from app.services import metric_services
from app.utils.serialization import serialize_many
from app.utils.validation import validate_metric_payload, validate_metric_update_payload


class MetricsResource(MethodView):

    def get(self):
        server_id = request.args.get("server_id")
        if server_id:
            metrics = metric_services.find_metrics_by_server(server_id)
        else:
            metrics = metric_services.find_all_metrics()
        return jsonify(serialize_many(metrics)), 200

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


class MetricDetailResource(MethodView):

    def put(self, metric_id: str):
        payload = request.get_json(silent=True) or {}
        ok, error_message = validate_metric_payload(payload)
        if not ok:
            return jsonify({"error": error_message}), 400

        try:
            modified = metric_services.replace_metric(metric_id, payload)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        if modified == 0:
            return jsonify({"error": "Métrica no encontrada"}), 404
        return jsonify({"message": "Métrica actualizada correctamente"}), 200

    def patch(self, metric_id: str):
        payload = request.get_json(silent=True) or {}
        ok, error_message = validate_metric_update_payload(payload)
        if not ok:
            return jsonify({"error": error_message}), 400

        try:
            modified = metric_services.update_metric_by_id(metric_id, payload)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        if modified == 0:
            return jsonify({"error": "Métrica no encontrada"}), 404
        return jsonify({"message": "Métrica actualizada correctamente"}), 200

    def delete(self, metric_id: str):
        try:
            deleted = metric_services.delete_metric_by_id(metric_id)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        if deleted == 0:
            return jsonify({"error": "Métrica no encontrada"}), 404
        return "", 204


__all__ = ["MetricsResource", "MetricDetailResource"]
