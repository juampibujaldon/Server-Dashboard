from flask import Blueprint

from app.resources import MetricDetailResource, MetricsResource

api = Blueprint("api", __name__)

metrics_view = MetricsResource.as_view("metrics")
api.add_url_rule("/metrics", view_func=metrics_view, methods=["GET", "POST"])

metric_detail_view = MetricDetailResource.as_view("metric_detail")
api.add_url_rule(
    "/metrics/<string:metric_id>",
    view_func=metric_detail_view,
    methods=["PUT", "PATCH", "DELETE"],
)
