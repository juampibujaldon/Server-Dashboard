import os
import pytest
from pymongo import MongoClient

os.environ['BACKEND_ENV'] = 'testing'

from app import create_app
from config.config import TestConfig

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
    
    client = MongoClient(TestConfig.MONGO_URI)
    client.drop_database(client.get_database().name)
    print("\nBase de datos de prueba eliminada.")

def test_metrics_submission_endpoint(test_client):
    db_client = MongoClient(TestConfig.MONGO_URI)
    db = db_client.get_database()
    db.metrics.delete_many({}) 

    mock_metric = {
        "serverId": "server-integration-test-01",
        "cpu_usage": 88.0,
        "ram_usage": 72.5,
        "disk_space": 91.3,
        "temperature": 75.0
    }
    
    response = test_client.post('/api/metrics', json=mock_metric)
    
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

    metric_from_db = db.metrics.find_one({"serverId": "server-integration-test-01"})
    assert metric_from_db is not None
    assert metric_from_db['cpu_usage'] == 88.0