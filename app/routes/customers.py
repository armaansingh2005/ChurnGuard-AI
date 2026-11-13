from flask import Blueprint, jsonify, render_template
from flask_login import login_required

from app import db
from app.models.database_models import Customer

customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/customers")
@login_required
def customers_page():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return render_template("customers.html", customers=customers)


@customers_bp.route("/api/customers")
@login_required
def api_customers():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return jsonify({
        "success": True,
        "count": len(customers),
        "data": [{
            "id": c.id,
            "customer_id": c.customer_id,
            "attributes": c.customer_attributes,
            "created_at": c.created_at.isoformat()
        } for c in customers]
    })
