from bson import ObjectId

from app.models.alert import Alert
from app.services import alert_services as svc


def test_create_and_get_by_id(db):
    aid = svc.create_alert(Alert("srv-1", "cpu_usage", 80.0, ">"))
    assert aid
    doc = svc.get_alert_by_id(aid)
    assert doc["metric_type"] == "cpu_usage"

def test_list_by_server_and_update(db):
    svc.create_alert(Alert("srv-a", "ram_usage", 70.0, ">="))
    svc.create_alert(Alert("srv-a", "disk_space", 90.0, ">"))
    out = svc.list_alerts_by_server("srv-a")
    assert len(out) >= 2
    aid = str(out[0]["_id"])
    modified = svc.update_alert(aid, {"threshold": 75.5})
    assert modified in (0, 1)

def test_delete_alert(db):
    aid = svc.create_alert(Alert("srv-d", "temperature", 60.0, ">"))
    deleted = svc.delete_alert(aid)
    assert deleted == 1
    assert db.alerts.find_one({"_id": ObjectId(aid)}) is None
