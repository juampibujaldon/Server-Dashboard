from bson import ObjectId

from app.models.server import Server
from app.services import server_services as svc


def test_create_and_get(db):
    sid = svc.create_server(Server("s1", "10.0.0.1", "active"))
    assert sid
    doc = svc.get_server_by_id(sid)
    assert doc["name"] == "s1"

def test_list_and_update(db):
    svc.create_server(Server("s2", "10.0.0.2", "inactive"))
    out = svc.list_servers()
    assert len(out) >= 2
    sid = str(out[0]["_id"])
    modified = svc.update_server(sid, {"status": "maintenance"})
    assert modified in (0, 1)

def test_delete(db):
    sid = svc.create_server(Server("s3", "10.0.0.3", "active"))
    deleted = svc.delete_server(sid)
    assert deleted == 1
    assert db.servers.find_one({"_id": ObjectId(sid)}) is None
