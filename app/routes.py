from flask import Blueprint, request, jsonify, current_app

api = Blueprint('api', __name__)

@api.route('/metrics', methods=['POST'])
def receive_metrics():
    data = request.get_json()

    if not data or 'serverId' not in data:
        return jsonify({"error": "Datos incompletos o en formato incorrecto"}), 400

    db = current_app.db
    
    db.metrics.insert_one(data)

    return jsonify({"status": "ok", "message": "Métrica recibida correctamente"}), 200