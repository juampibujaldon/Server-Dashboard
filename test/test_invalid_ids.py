import pytest
from app.services import metric_services as metrics


def test_update_metric_with_invalid_id_raises_value_error(db):
    with pytest.raises(ValueError):
        metrics.update_metric_by_id("not-a-valid-objectid", {"cpu_usage": 1})


def test_delete_metric_with_invalid_id_raises_value_error(db):
    with pytest.raises(ValueError):
        metrics.delete_metric_by_id("invalid-id")

