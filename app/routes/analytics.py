from flask import Blueprint, jsonify, render_template
from flask_login import login_required

from app.services.analytics_service import get_analytics_data

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
@login_required
def analytics_page():
    data = get_analytics_data()
    return render_template("analytics.html", data=data)


@analytics_bp.route("/api/analytics")
@login_required
def api_analytics():
    return jsonify(get_analytics_data())
