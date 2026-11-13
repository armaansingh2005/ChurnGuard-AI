from flask import Blueprint, render_template
from flask_login import login_required

from app.services.analytics_service import get_dashboard_metrics


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard_page():
    metrics = get_dashboard_metrics()
    return render_template("dashboard.html", metrics=metrics)
