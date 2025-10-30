from datetime import datetime

from app.services.metric_services import ARGENTINA_DATETIME_FORMAT


def test_metrics_get_endpoint_serialization(client, db):
    payload = {"server_id":"srv-get-01","cpu_usage":10.0,"ram_usage":20.0,"disk_space":30.0,"temperature":40.0}
    r = client.post("/api/metrics", json=payload)
    assert r.status_code == 201

    r2 = client.get("/api/metrics/srv-get-01")
    assert r2.status_code == 200
    data = r2.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    first = data[0]
    # Debe existir 'id' serializado y no '_id'
    assert "id" in first
    assert "_id" not in first
    assert "sent_at" in first
    datetime.strptime(first["sent_at"], ARGENTINA_DATETIME_FORMAT)
