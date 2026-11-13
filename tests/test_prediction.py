import pandas as pd

from app.models.ml_model import predict_customer, risk_category_from_probability


def test_risk_category_thresholds():
    assert risk_category_from_probability(0.2) == "Low"
    assert risk_category_from_probability(0.5) == "Medium"
    assert risk_category_from_probability(0.8) == "High"


def test_prediction_api_output():
    sample = {
        "customerID": "TEST-001",
        "gender": "Male",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "tenure": 12,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "Yes",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 78.0,
        "TotalCharges": 900.0,
    }
    result = predict_customer(sample)
    assert "churn_prediction" in result
    assert "churn_probability" in result
    assert 0 <= result["churn_probability"] <= 100
