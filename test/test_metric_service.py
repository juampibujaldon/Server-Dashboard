from datetime import datetime
from bson import ObjectId
from app.models.metric import Metric
from app.services import metric_services as svc

def test_create_and_list_by_server(db):
    m = Metric("srv-1", 70.0, 60.0, 80.0, 50.0).to_dict()
    mid = svc.save_metric(m)
    assert mid
    out = svc.find_metrics_by_server("srv-1")
    assert isinstance(out, list)
    assert len(out) >= 1
    assert out[0]["server_id"] == "srv-1"
    doc = db.metrics.find_one({"_id": ObjectId(mid)})
    assert doc is not None
    sent_at = doc.get("sent_at")
    assert isinstance(sent_at, str)
    # Fecha y hora locales (AR) para trazabilidad
    datetime.strptime(sent_at, svc.ARGENTINA_DATETIME_FORMAT)

def test_update_by_id(db):
    mid = svc.save_metric(Metric("srv-upd", 1.0, 2.0, 3.0, 4.0).to_dict())
    modified = svc.update_metric_by_id(mid, {"cpu_usage": 99.9})
    assert modified == 1
    doc = db.metrics.find_one({"_id": ObjectId(mid)})
    assert doc["cpu_usage"] == 99.9

def test_delete_by_id(db):
    mid = svc.save_metric(Metric("srv-del", 1, 2, 3, 4).to_dict())
    deleted = svc.delete_metric_by_id(mid)
    assert deleted == 1
    assert db.metrics.find_one({"_id": ObjectId(mid)}) is None

def test_delete_by_server(db):
    svc.save_metric(Metric("srv-x", 1, 2, 3, 4).to_dict())
    svc.save_metric(Metric("srv-x", 5, 6, 7, 8).to_dict())
    deleted = svc.delete_metrics_by_server("srv-x")
    assert deleted >= 2
    assert db.metrics.count_documents({"server_id": "srv-x"}) == 0
