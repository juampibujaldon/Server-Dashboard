def test_metrics_submission_endpoint(client, db):
    payload = {"serverId":"server-integration-test-01","cpu_usage":88.0,"ram_usage":72.5,"disk_space":91.3,"temperature":75.0}
    r = client.post("/api/metrics", json=payload)
    assert r.status_code == 201
    assert r.get_json()["message"] == "Métrica añadida correctamente"
    doc = db.metrics.find_one({"serverId":"server-integration-test-01"})
    assert doc is not None
    assert doc["cpu_usage"] == 88.0
