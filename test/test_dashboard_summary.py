import pytest


def test_dashboard_summary_without_metrics(client, db):
    db.metrics.delete_many({})

    resp = client.get("/api/dashboard/summary")

    assert resp.status_code == 200
    data = resp.get_json()

    assert data["summary"]["totalServers"] == 0
    assert data["summary"]["totalMetrics"] == 0
    assert data["summary"]["avgCpu"] is None
    assert data["servers"] == []
    assert data["statusCounts"] == {"ok": 0, "warning": 0, "critical": 0}


@pytest.mark.parametrize(
    "payloads",
    [
        [
            {"server_id": "srv-app-01", "cpu_usage": 45.0, "ram_usage": 50.0, "disk_space": 60.0, "temperature": 45.0},
            {"server_id": "srv-app-01", "cpu_usage": 88.0, "ram_usage": 70.0, "disk_space": 75.0, "temperature": 78.0},
            {"server_id": "srv-db-02", "cpu_usage": 95.0, "ram_usage": 92.0, "disk_space": 97.0, "temperature": 90.0},
        ]
    ],
)
def test_dashboard_summary_with_metrics(client, db, payloads):
    db.metrics.delete_many({})

    for payload in payloads:
        resp = client.post("/api/metrics", json=payload)
        assert resp.status_code == 201

    resp = client.get("/api/dashboard/summary")
    assert resp.status_code == 200

    data = resp.get_json()
    summary = data["summary"]

    assert summary["totalServers"] == 2
    assert summary["totalMetrics"] == 3
    assert summary["avgCpu"] == pytest.approx(76.0, rel=1e-3)
    assert summary["avgRam"] == pytest.approx(70.67, rel=1e-3)
    assert summary["avgDisk"] == pytest.approx(77.33, rel=1e-3)
    assert summary["avgTemperature"] == pytest.approx(71.0, rel=1e-3)

    assert data["statusCounts"] == {"ok": 0, "warning": 1, "critical": 1}

    servers = {s["serverId"]: s for s in data["servers"]}
    assert set(servers.keys()) == {"srv-app-01", "srv-db-02"}

    srv_app = servers["srv-app-01"]
    assert srv_app["status"] == "warning"
    assert srv_app["latest"]["cpu"] == pytest.approx(88.0)
    assert len(srv_app["trend"]) == 2
    assert srv_app["averages"]["cpu"] == pytest.approx(66.5)

    srv_db = servers["srv-db-02"]
    assert srv_db["status"] == "critical"
    assert srv_db["latest"]["cpu"] == pytest.approx(95.0)
    assert len(srv_db["trend"]) == 1
