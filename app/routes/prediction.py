from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import login_required

from app.models.ml_model import predict_customer, predict_dataframe, risk_category_from_probability
from app.services.data_service import validate_customer_payload, validate_csv_upload

prediction_bp = Blueprint("prediction", __name__)


@prediction_bp.route("/predict", methods=["GET", "POST"])
@login_required
def predict_page():
    result = None
    if request.method == "POST":
        payload = {
            "customerID": request.form.get("customerID", "CUST-0001"),
            "gender": request.form.get("gender", "Male"),
            "SeniorCitizen": int(request.form.get("SeniorCitizen", 0) or 0),
            "Partner": request.form.get("Partner", "No"),
            "Dependents": request.form.get("Dependents", "No"),
            "tenure": int(request.form.get("tenure", 1) or 1),
            "PhoneService": request.form.get("PhoneService", "Yes"),
            "MultipleLines": request.form.get("MultipleLines", "No"),
            "InternetService": request.form.get("InternetService", "Fiber optic"),
            "OnlineSecurity": request.form.get("OnlineSecurity", "No"),
            "OnlineBackup": request.form.get("OnlineBackup", "No"),
            "DeviceProtection": request.form.get("DeviceProtection", "No"),
            "TechSupport": request.form.get("TechSupport", "No"),
            "StreamingTV": request.form.get("StreamingTV", "No"),
            "StreamingMovies": request.form.get("StreamingMovies", "No"),
            "Contract": request.form.get("Contract", "Month-to-month"),
            "PaperlessBilling": request.form.get("PaperlessBilling", "Yes"),
            "PaymentMethod": request.form.get("PaymentMethod", "Electronic check"),
            "MonthlyCharges": float(request.form.get("MonthlyCharges", 0) or 0),
            "TotalCharges": float(request.form.get("TotalCharges", 0) or 0),
        }
        errors = validate_customer_payload(payload)
        if errors:
            flash("; ".join(errors), "danger")
        else:
            result = predict_customer(payload)
    return render_template("prediction.html", result=result)


@prediction_bp.route("/bulk-predict", methods=["GET", "POST"])
@login_required
def bulk_predict_page():
    if request.method == "POST":
        file = request.files.get("csv_file")
        if not file:
            flash("Please upload a CSV file.", "danger")
            return render_template("bulk_prediction.html")
        validation = validate_csv_upload(file)
        if not validation["valid"]:
            flash(validation["message"], "danger")
            return render_template("bulk_prediction.html")
        df = validation["dataframe"]
        results = predict_dataframe(df)
        return render_template("bulk_prediction.html", results=results.to_dict(orient="records"), total_rows=len(results))
    return render_template("bulk_prediction.html")


@prediction_bp.route("/api/predict", methods=["POST"])
@login_required
def api_predict():
    payload = request.get_json(silent=True) or {}
    errors = validate_customer_payload(payload)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400
    result = predict_customer(payload)
    return jsonify({"success": True, "data": result})


@prediction_bp.route("/api/bulk-predict", methods=["POST"])
@login_required
def api_bulk_predict():
    file = request.files.get("file")
    if not file:
        return jsonify({"success": False, "message": "No file uploaded."}), 400
    validation = validate_csv_upload(file)
    if not validation["valid"]:
        return jsonify({"success": False, "message": validation["message"]}), 400
    results = predict_dataframe(validation["dataframe"])
    return jsonify({"success": True, "count": len(results), "data": results.to_dict(orient="records")})
