import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from config import BASE_DIR

DATASET_PATH = BASE_DIR / "data" / "raw" / "Telco-Customer-Churn.csv"
ARTIFACT_DIR = BASE_DIR / "ml" / "model_artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset():
    df = pd.read_csv(DATASET_PATH)
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)
    df["Churn"] = df["Churn"].str.strip().str.lower().eq("yes").astype(int)
    return df


def build_model_pipeline(model_name):
    categorical_features = [
        "gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
        "Contract", "PaperlessBilling", "PaymentMethod"
    ]
    numeric_features = ["tenure", "MonthlyCharges", "TotalCharges"]
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric_features),
            ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical_features),
        ]
    )

    models = {
        "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "decision_tree": DecisionTreeClassifier(class_weight="balanced"),
        "random_forest": RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced"),
        "svm": SVC(probability=True, class_weight="balanced", random_state=42),
        "gradient_boosting": GradientBoostingClassifier(random_state=42),
    }
    model = models[model_name]
    pipeline = Pipeline([("preprocessor", preprocessor), ("model", model)])
    return pipeline


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    score = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_prob),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }
    return score


def train_and_save_models():
    df = load_dataset()
    feature_columns = [
        "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
        "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges"
    ]
    X = df[feature_columns]
    y = df["Churn"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model_names = ["logistic_regression", "decision_tree", "random_forest", "svm", "gradient_boosting"]
    results = {}
    best_model_name = None
    best_score = -1

    for name in model_names:
        pipeline = build_model_pipeline(name)
        pipeline.fit(X_train, y_train)
        score = evaluate_model(pipeline, X_test, y_test)
        results[name] = score
        if score["roc_auc"] > best_score:
            best_score = score["roc_auc"]
            best_model_name = name

    if best_model_name is None:
        raise RuntimeError("No model could be trained successfully.")

    final_pipeline = build_model_pipeline(best_model_name)
    final_pipeline.fit(X, y)
    joblib.dump(final_pipeline, ARTIFACT_DIR / "best_model.joblib")
    metadata = {
        "model_version": best_model_name,
        "feature_columns": feature_columns,
        "training_rows": len(X),
        "test_rows": len(X_test),
        "best_model_name": best_model_name,
        "results": results,
    }
    with open(ARTIFACT_DIR / "metadata.json", "w") as fh:
        json.dump(metadata, fh, indent=2)

    # Save the preprocessor separately for use in prediction service.
    joblib.dump(final_pipeline.named_steps["preprocessor"], ARTIFACT_DIR / "preprocessor.joblib")
    return metadata


if __name__ == "__main__":
    meta = train_and_save_models()
    print(json.dumps(meta["results"], indent=2))
