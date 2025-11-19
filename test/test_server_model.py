from dataclasses import asdict

import pytest

from app.models.server import Server


@pytest.fixture
def server_sample():
    return Server(name="web-server-01", ip_address="192.168.1.100", status="active")

def test_id_is_none_by_default(server_sample):
    assert server_sample.id is None

def test_fields_are_assigned(server_sample):
    assert server_sample.name == "web-server-01"
    assert server_sample.ip_address == "192.168.1.100"
    assert server_sample.status == "active"

def test_asdict_contains_all_fields(server_sample):
    d = asdict(server_sample)
    assert set(d.keys()) == {"name", "ip_address", "status", "id"}
    assert d["name"] == "web-server-01"

def test_value_equality_and_copy():
    a = Server("web-server-01", "192.168.1.100", "active")
    b = Server("web-server-01", "192.168.1.100", "active")
    c = Server("web-server-01", "192.168.1.100", "inactive")
    assert a == b
    assert a != c
    assert a == Server(**asdict(a))

@pytest.mark.parametrize("status", ["active", "inactive", "maintenance"])
def test_status_values(status):
    s = Server("s", "10.0.0.1", status)
    assert s.status == status
