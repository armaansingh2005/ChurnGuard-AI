import json
from pathlib import Path

import joblib
import pandas as pd

from config import BASE_DIR

MODEL_PATH = BASE_DIR / "ml" / "model_artifacts" / "best_model.joblib"
PREPROCESSOR_PATH = BASE_DIR / "ml" / "model_artifacts" / "preprocessor.joblib"
METADATA_PATH = BASE_DIR / "ml" / "model_artifacts" / "metadata.json"


def risk_category_from_probability(probability):
    if probability < 0.3:
        return "Low"
    if probability < 0.7:
        return "Medium"
    return "High"


def _load_model_bundle():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Trained model artifacts are missing. Please run the training workflow first.")
    model = joblib.load(MODEL_PATH)
    metadata = json.loads(METADATA_PATH.read_text()) if METADATA_PATH.exists() else {}
    return model, metadata


def feature_order():
    return [
        "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService", "MultipleLines",
        "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod",
        "MonthlyCharges", "TotalCharges"
    ]


def _normalize_payload(payload):
    data = {key: (payload.get(key) if payload.get(key) is not None else "") for key in feature_order()}
    for key in ["gender", "Partner", "Dependents", "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod"]:
        if data.get(key) in (None, ""):
            if key == "gender":
                data[key] = "Male"
            elif key in {"OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"}:
                data[key] = "No"
            else:
                data[key] = "No"
    data["SeniorCitizen"] = int(data.get("SeniorCitizen", 0) or 0)
    data["tenure"] = int(data.get("tenure", 1) or 1)
    data["MonthlyCharges"] = float(data.get("MonthlyCharges", 0) or 0)
    data["TotalCharges"] = float(data.get("TotalCharges", 0) or 0)
    return pd.DataFrame([data], columns=feature_order())


def predict_customer(payload):
    model, metadata = _load_model_bundle()
    df = _normalize_payload(payload)
    prob = model.predict_proba(df)[0, 1]
    prediction = bool(model.predict(df)[0])
    risk = risk_category_from_probability(prob)
    response = {
        "customerID": payload.get("customerID", "N/A"),
        "churn_prediction": prediction,
        "churn_probability": round(float(prob) * 100, 2),
        "risk_category": risk,
        "model_version": metadata.get("model_version", "v1"),
        "thresholds": {"low": 30, "medium": 70},
        "explanation": "Probability generated from the trained churn model using the same preprocessing pipeline used during training.",
    }
    return response


def predict_dataframe(df):
    model, metadata = _load_model_bundle()
    required = feature_order()
    for column in required:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")
    frame = df.copy()
    frame = frame[required]
    if "TotalCharges" in frame.columns:
        frame["TotalCharges"] = pd.to_numeric(frame["TotalCharges"].replace(" ", pd.NA), errors="coerce").fillna(0)
    if "MonthlyCharges" in frame.columns:
        frame["MonthlyCharges"] = pd.to_numeric(frame["MonthlyCharges"], errors="coerce").fillna(0)
    frame["SeniorCitizen"] = pd.to_numeric(frame["SeniorCitizen"], errors="coerce").fillna(0).astype(int)
    frame["tenure"] = pd.to_numeric(frame["tenure"], errors="coerce").fillna(1).astype(int)
    probs = model.predict_proba(frame)[:, 1]
    preds = model.predict(frame)
    results = pd.DataFrame({
        "customerID": df.get("customerID", range(len(df))),
        "prediction": preds,
        "churn_probability": probs * 100,
        "risk_category": [risk_category_from_probability(p) for p in probs],
    })
    results["customerID"] = results["customerID"].astype(str)
    results["churn_prediction"] = results["prediction"].astype(bool)
    results["churn_probability"] = results["churn_probability"].round(2)
    return results
