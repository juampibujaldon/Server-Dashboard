from bson import ObjectId

from app.models.metric import Metric


def test_create_metric(db):
    doc = Metric("srv-crud", 10.0, 20.0, 30.0, 40.0).to_dict()
    res = db.metrics.insert_one(doc)
    assert res.inserted_id is not None

def test_read_metrics(db):
    db.metrics.insert_many([
        Metric("srv-crud", 11.0, 21.0, 31.0, 41.0).to_dict(),
        Metric("srv-other", 50.0, 60.0, 70.0, 80.0).to_dict(),
    ])
    docs = list(db.metrics.find({"server_id": "srv-crud"}))
    assert len(docs) >= 2

def test_update_metric(db):
    db.metrics.insert_one(Metric("srv-upd", 1.0, 2.0, 3.0, 4.0).to_dict())
    res = db.metrics.update_one({"server_id": "srv-upd"}, {"$set": {"cpu_usage": 9.9}})
    assert res.modified_count == 1
    doc = db.metrics.find_one({"server_id": "srv-upd"})
    assert doc["cpu_usage"] == 9.9

def test_delete_metric(db):
    db.metrics.insert_one(Metric("srv-del", 1.0, 2.0, 3.0, 4.0).to_dict())
    res = db.metrics.delete_one({"server_id": "srv-del"})
    assert res.deleted_count == 1
    assert db.metrics.find_one({"server_id": "srv-del"}) is None
