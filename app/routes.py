from flask import Blueprint, request, jsonify
from .services import metric_services as metric_service

api = Blueprint("api", __name__)

@api.route("/metrics", methods=["POST"])
def add_metric():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de la petición inválido"}), 400
    try:
        metric_service.save_metric(data)
        return jsonify({"message": "Métrica añadida correctamente"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Ocurrió un error en el servidor"}), 500

@api.route("/metrics/<server_id>", methods=["GET"])
def get_metrics(server_id):
    metrics = metric_service.find_metrics_by_server(server_id)
    return jsonify(metrics), 200
