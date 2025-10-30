import pytest
from app.models.metric import Metric

@pytest.fixture
def metric_sample():
    return Metric(
        server_id="srv-1",
        cpu_usage=75.0,
        ram_usage=55.2,
        disk_space=90.1,
        temperature=68.5,
    )

def test_metric_id_defaults_to_none(metric_sample):
    assert metric_sample.id is None

def test_metric_fields(metric_sample):
    assert metric_sample.server_id == "srv-1"
    assert isinstance(metric_sample.cpu_usage, float)
    assert isinstance(metric_sample.ram_usage, float)
    assert isinstance(metric_sample.disk_space, float)
    assert isinstance(metric_sample.temperature, float)

def test_metric_to_dict(metric_sample):
    d = metric_sample.to_dict()
    assert set(d.keys()) == {"server_id", "cpu_usage", "ram_usage", "disk_space", "temperature", "id", "sent_at"}
    assert d["server_id"] == "srv-1"
    assert d["sent_at"] is None

def test_metric_value_equality():
    a = Metric("s", 1.0, 2.0, 3.0, 4.0)
    b = Metric("s", 1.0, 2.0, 3.0, 4.0)
    c = Metric("t", 1.0, 2.0, 3.0, 4.0)
    assert a == b
    assert a != c
