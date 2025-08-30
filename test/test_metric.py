import os
import pytest

from app import create_app
from app.db import db  

os.environ['BACKEND_ENV'] = 'testing'

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
    

    print("\nLimpiando la base de datos de prueba...")
    db.metrics.delete_many({})

def test_metrics_submission(self):
    mock_metric = {
        "serverId": "server-test-01",
        "cpu_usage": 75.0,
        "ram_usage": 55.2,
        "disk_space": 90.1,
        "temperature": 68.5
    }
    response = self.client.post("/api/metrics", json=mock_metric)
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

    metric_from_db = self.db.metrics.find_one({"serverId": "server-test-01"})
    assert metric_from_db is not None
    assert metric_from_db['cpu_usage'] == 88.0