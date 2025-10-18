from flask import Blueprint

from app.resources import (
    MetricsResource,
    MetricsByServerResource,
    DashboardSummaryResource,
)

api = Blueprint("api", __name__)

metrics_view = MetricsResource.as_view("metrics")
api.add_url_rule("/metrics", view_func=metrics_view, methods=["GET", "POST"])

metrics_by_server_view = MetricsByServerResource.as_view("metrics_by_server")
api.add_url_rule(
    "/metrics/<string:server_id>", view_func=metrics_by_server_view, methods=["GET"],
)

dashboard_summary_view = DashboardSummaryResource.as_view("dashboard_summary")
api.add_url_rule(
    "/dashboard/summary", view_func=dashboard_summary_view, methods=["GET"],
)
