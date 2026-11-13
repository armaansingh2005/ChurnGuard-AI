import pandas as pd
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"csv"}
REQUIRED_COLUMNS = [
    "customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService",
    "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
    "PaymentMethod", "MonthlyCharges", "TotalCharges"
]


def validate_customer_payload(payload):
    errors = []
    required_fields = [
        "customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
        "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
        "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
        "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges"
    ]
    for field in required_fields:
        if field not in payload or payload[field] in (None, ""):
            errors.append(f"Missing required field: {field}")
    if payload.get("MonthlyCharges") is not None:
        try:
            float(payload["MonthlyCharges"])
        except (TypeError, ValueError):
            errors.append("MonthlyCharges must be numeric.")
    if payload.get("TotalCharges") is not None:
        try:
            float(payload["TotalCharges"])
        except (TypeError, ValueError):
            errors.append("TotalCharges must be numeric.")
    return errors


def validate_csv_upload(file_storage):
    filename = secure_filename(file_storage.filename or "")
    if not filename or "." not in filename or filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
        return {"valid": False, "message": "Only CSV files are allowed."}

    try:
        df = pd.read_csv(file_storage)
    except Exception:
        return {"valid": False, "message": "Unable to read the uploaded CSV. Please check the file format."}

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return {"valid": False, "message": f"CSV is missing required columns: {', '.join(missing)}"}

    if df.empty:
        return {"valid": False, "message": "The uploaded CSV contains no rows."}

    return {"valid": True, "dataframe": df, "message": "CSV validated successfully."}
