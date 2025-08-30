import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from .services import metric_services as metric_service
from .db import db_manager

api = Blueprint('api', __name__)
auth_bp = Blueprint('auth', __name__)

def token_required(f):
    return f

@auth_bp.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({"message": "Faltan credenciales"}), 401

    admin_user = current_app.config.get('ADMIN_USERNAME')
    admin_pass = current_app.config.get('ADMIN_PASSWORD')

    if auth.get('username') == admin_user and auth.get('password') == admin_pass:
        token = jwt.encode({
            'user': auth.get('username'),
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})

    return jsonify({"message": "Credenciales incorrectas"}), 401


@api.route('/metrics', methods=['POST'])
@token_required
def add_metric():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de la petición inválido"}), 400
    
    try:
        metric_service.save_metric(data)
        return jsonify({"message": "Métrica añadida correctamente"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor"}), 500

@api.route('/metrics/<server_id>', methods=['GET'])
@token_required
def get_metrics(server_id):
    metrics = metric_service.find_metrics_by_server(server_id)
    return jsonify(metrics), 200