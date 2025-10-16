import pytest
from app.models.alert import Alert

@pytest.fixture
def alert_sample():
    return Alert(server_id="srv-1", metric_type="cpu_usage", threshold=80.0, condition=">")

def test_id_defaults_to_none(alert_sample):
    assert alert_sample.id is None

def test_fields(alert_sample):
    assert alert_sample.server_id == "srv-1"
    assert alert_sample.metric_type == "cpu_usage"
    assert isinstance(alert_sample.threshold, float)
    assert alert_sample.condition == ">"

def test_to_dict(alert_sample):
    d = alert_sample.to_dict()
    assert set(d.keys()) == {"server_id", "metric_type", "threshold", "condition", "id"}
    assert d["metric_type"] == "cpu_usage"

def test_value_equality():
    a = Alert("s", "cpu_usage", 80.0, ">")
    b = Alert("s", "cpu_usage", 80.0, ">")
    c = Alert("s", "ram_usage", 80.0, ">")
    assert a == b
    assert a != c

@pytest.mark.parametrize("condition", [">", ">=", "<", "<=", "=="])
def test_condition_variants(condition):
    a = Alert("s", "cpu_usage", 70.0, condition)
    assert a.condition == condition

@pytest.mark.parametrize("metric_type", ["cpu_usage", "ram_usage", "disk_space", "temperature"])
def test_metric_type_variants(metric_type):
    a = Alert("s", metric_type, 70.0, ">")
    assert a.metric_type == metric_type

@pytest.mark.parametrize("threshold", [0.0, 50.0, 99.999, 100.0])
def test_threshold_boundaries(threshold):
    a = Alert("s", "cpu_usage", threshold, ">")
    assert a.threshold == pytest.approx(threshold)
