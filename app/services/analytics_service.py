from pathlib import Path

import pandas as pd

from config import BASE_DIR

DATASET_PATH = BASE_DIR / "data" / "raw" / "Telco-Customer-Churn.csv"


def load_dataset():
    df = pd.read_csv(DATASET_PATH)
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)
    df["Churn"] = df["Churn"].str.strip().str.lower().eq("yes").astype(int)
    return df


def get_dashboard_metrics():
    df = load_dataset()
    total_customers = len(df)
    churned = int(df["Churn"].sum())
    active_customers = total_customers - churned
    churn_rate = round((churned / total_customers) * 100, 2) if total_customers else 0
    high_risk = int((df["Churn"] == 1).sum() * 0.2)
    avg_monthly = round(df["MonthlyCharges"].mean(), 2)
    return {
        "total_customers": total_customers,
        "churned_customers": churned,
        "active_customers": active_customers,
        "overall_churn_rate": churn_rate,
        "high_risk_customers": high_risk,
        "average_monthly_charges": avg_monthly,
    }


def get_analytics_data():
    df = load_dataset()
    churn_distribution = {
        "labels": ["Retained", "Churned"],
        "values": [int((1 - df["Churn"]).sum()), int(df["Churn"].sum())],
    }
    contract_churn = (
        df.groupby("Contract", dropna=False)["Churn"].mean().sort_values(ascending=False).round(4).to_dict()
    )
    tenure_churn = (
        df.groupby("tenure")["Churn"].mean().round(4).to_dict()
    )
    payment_churn = (
        df.groupby("PaymentMethod", dropna=False)["Churn"].mean().sort_values(ascending=False).round(4).to_dict()
    )
    return {
        "metrics": get_dashboard_metrics(),
        "charts": {
            "churn_distribution": churn_distribution,
            "contract_churn": contract_churn,
            "tenure_churn": tenure_churn,
            "payment_churn": payment_churn,
        },
    }
