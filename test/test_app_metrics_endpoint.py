from bson import ObjectId

from app.services import metric_services as svc


def test_metrics_submission_endpoint(client, db):
    payload = {"server_id":"server-integration-test-01","cpu_usage":88.0,"ram_usage":72.5,"disk_space":91.3,"temperature":75.0}
    r = client.post("/api/metrics", json=payload)
    assert r.status_code == 201
    assert r.get_json()["message"] == "Métrica añadida correctamente"
    doc = db.metrics.find_one({"server_id":"server-integration-test-01"})
    assert doc is not None
    assert doc["cpu_usage"] == 88.0


def test_metrics_put_endpoint(client, db):
    metric_id = svc.save_metric({"server_id": "srv-put", "cpu_usage": 10.0, "ram_usage": 15.0, "disk_space": 20.0, "temperature": 30.0})
    before = db.metrics.find_one({"_id": ObjectId(metric_id)})

    update_payload = {"server_id": "srv-put", "cpu_usage": 50.0, "ram_usage": 40.0, "disk_space": 60.0, "temperature": 45.0}
    response = client.put(f"/api/metrics/{metric_id}", json=update_payload)

    assert response.status_code == 200
    assert response.get_json()["message"] == "Métrica actualizada correctamente"

    after = db.metrics.find_one({"_id": ObjectId(metric_id)})
    assert after["cpu_usage"] == 50.0
    assert after["ram_usage"] == 40.0
    assert after["disk_space"] == 60.0
    assert after["temperature"] == 45.0
    assert isinstance(after["sent_at"], str)


def test_metrics_patch_endpoint(client, db):
    metric_id = svc.save_metric({"server_id": "srv-patch", "cpu_usage": 10.0, "ram_usage": 15.0, "disk_space": 20.0, "temperature": 30.0})

    response = client.patch(f"/api/metrics/{metric_id}", json={"cpu_usage": 25.5})

    assert response.status_code == 200
    assert response.get_json()["message"] == "Métrica actualizada correctamente"

    doc = db.metrics.find_one({"_id": ObjectId(metric_id)})
    assert doc["cpu_usage"] == 25.5
    assert doc["ram_usage"] == 15.0  # resto permanece


def test_metrics_delete_endpoint(client, db):
    metric_id = svc.save_metric({"server_id": "srv-delete", "cpu_usage": 10.0, "ram_usage": 15.0, "disk_space": 20.0, "temperature": 30.0})

    response = client.delete(f"/api/metrics/{metric_id}")

    assert response.status_code == 204
    assert db.metrics.find_one({"_id": ObjectId(metric_id)}) is None
