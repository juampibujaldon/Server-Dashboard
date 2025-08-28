from flask import Blueprint, request, jsonify, current_app  
from db import db


api = Blueprint('api', __name__)

@api.route('/')
def home():
    return jsonify({"message": "API de monitoreo funcionando!"})

@api.route('/status')
def status():
    return jsonify({"status": "ok"})

@api.route('/metrics', methods=['POST'])
def submit_metrics():    
    data = request.get_json()
    
    if not data or 'serverId' not in data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400
        
    db.metrics.insert_one(data)
    
    return jsonify({"status": "ok"})