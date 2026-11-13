from flask import Blueprint, jsonify, render_template
from flask_login import login_required

from app import db
from app.models.database_models import Prediction

history_bp = Blueprint("history", __name__)


@history_bp.route("/history")
@login_required
def history_page():
    records = Prediction.query.order_by(Prediction.created_at.desc()).all()
    return render_template("history.html", records=records)


@history_bp.route("/api/predictions")
@login_required
def api_predictions():
    rows = Prediction.query.order_by(Prediction.created_at.desc()).all()
    return jsonify({
        "success": True,
        "count": len(rows),
        "data": [{
            "id": r.id,
            "customer_id": r.customer_id,
            "churn_prediction": r.churn_prediction,
            "churn_probability": r.churn_probability,
            "risk_category": r.risk_category,
            "model_version": r.model_version,
            "created_at": r.created_at.isoformat()
        } for r in rows]
    })
