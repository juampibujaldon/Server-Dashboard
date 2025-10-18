import json
from flask import Blueprint, render_template

from app.services.dashboard_service import get_dashboard_summary


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
def home():
    data = get_dashboard_summary()
    payload = json.dumps(data, ensure_ascii=False)
    return render_template("dashboard.html", dashboard_data=payload)

