def test_metrics_post_missing_field_returns_400(client):
    bad = {"server_id":"s","cpu_usage":1.0,"ram_usage":2.0,"disk_space":3.0}  # falta temperature
    r = client.post("/api/metrics", json=bad)
    assert r.status_code == 400
    assert "Falta el campo" in r.get_json()["error"]


def test_metrics_post_out_of_range_returns_400(client):
    bad = {"server_id":"s","cpu_usage":150.0,"ram_usage":2.0,"disk_space":3.0,"temperature":10.0}
    r = client.post("/api/metrics", json=bad)
    assert r.status_code == 400
    assert "entre 0 y 100" in r.get_json()["error"]
