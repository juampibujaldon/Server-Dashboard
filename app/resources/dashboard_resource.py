from flask import jsonify
from flask.views import MethodView

from app.services.dashboard_service import get_dashboard_summary


class DashboardSummaryResource(MethodView):
    def get(self):
        summary = get_dashboard_summary()
        return jsonify(summary), 200


__all__ = ["DashboardSummaryResource"]

