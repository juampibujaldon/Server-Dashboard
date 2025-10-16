from flask import Blueprint

from app.resources import MetricsResource, MetricsByServerResource

api = Blueprint("api", __name__)

metrics_view = MetricsResource.as_view("metrics")
api.add_url_rule("/metrics", view_func=metrics_view, methods=["GET", "POST"])

metrics_by_server_view = MetricsByServerResource.as_view("metrics_by_server")
api.add_url_rule(
    "/metrics/<string:server_id>", view_func=metrics_by_server_view, methods=["GET"],
)
