import datetime
from ..db import db_manager

def save_metric(data):
    db = db_manager.get_db()
    
    server_id = data.get('serverId')
    cpu_usage = data.get('cpu_usage')
    ram_usage = data.get('ram_usage')

    if not all([server_id, cpu_usage, ram_usage]):
        raise ValueError("Faltan datos en la métrica")

    metric_collection = db.metrics
    result = metric_collection.insert_one({
        "serverId": server_id,
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "timestamp": datetime.datetime.now(datetime.timezone.utc)
    })
    
    return result.inserted_id

def find_metrics_by_server(server_id):
    db = db_manager.get_db()
    metrics = list(db.metrics.find({"serverId": server_id}, {'_id': 0}))
    return metrics