import os
import unittest

os.environ['BACKEND_ENV'] = 'testing'

from app import create_app

class MetricsEndpointTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        self.db = self.app.db
        
        self.db.metrics.delete_many({})

    def tearDown(self):
        self.db.metrics.delete_many({})
        self.app_context.pop()

    def test_metrics_submission(self):
        mock_metric = {
            "serverId": "server-test-01",
            "cpu_usage": 75.0,
            "ram_usage": 55.2,
            "disk_space": 90.1,
            "temperature": 68.5
        }
        response = self.client.post("/api/metrics", json=mock_metric)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

        metric_from_db = self.db.metrics.find_one({"serverId": "server-test-01"})
        self.assertIsNotNone(metric_from_db)
        self.assertEqual(metric_from_db["cpu_usage"], 75.0)