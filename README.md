# ChurnGuard AI

ChurnGuard AI is a full-stack customer churn prediction and retention intelligence platform built with Flask, SQLAlchemy, scikit-learn, and modern frontend tooling. The system loads the IBM Telco Customer Churn dataset, preprocesses and models churn risk, and exposes both a web dashboard and API endpoints for prediction and analytics.

## Features

- Single-customer churn prediction with probability and risk classification
- Bulk CSV prediction workflow
- Executive dashboard with churn metrics and analytics
- SQLite database for customers and prediction history
- Model training and comparison pipeline using scikit-learn
- Retention recommendation logic based on customer attributes
- Secure login and registration system
- Responsive, SaaS-style UI

## Dataset

The project uses the IBM Telco Customer Churn dataset from the official IBM public data repository. It contains customer lifecycle attributes such as tenure, contract type, payment method, monthly charges, and churn status.

## Tech Stack

- Python 3.12+
- Flask
- SQLAlchemy
- scikit-learn
- pandas
- numpy
- XGBoost
- SHAP
- Plotly
- SQLite

## Installation

### Windows PowerShell

Run these commands from the project folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

If PowerShell prevents environment activation, run the environment's Python directly:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run.py
```

### macOS / Linux

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

## Open the app

Once Flask reports that it is running, open <http://127.0.0.1:5000/login>.
The first local run creates the SQLite database and trains the model from the
included dataset if model artifacts are missing. Keep the terminal open while
using the application.

The initial local account is `admin` / `admin123`. Change or remove the
development account before exposing the app to a network.

## Troubleshooting

- **Page cannot be reached:** Start the server with `python run.py` from this
  project folder, then use <http://127.0.0.1:5000/login>. The server must remain
  running in the terminal.
- **Missing Python packages:** Install dependencies using
  `python -m pip install -r requirements.txt` with the same Python environment
  used to run `run.py`.
- **Model artifacts missing:** Run `python -m ml.train` from the project folder.
- **Dataset missing:** Restore `data/raw/Telco-Customer-Churn.csv` from the
  IBM Telco Customer Churn dataset; the project does not generate substitute
  customer records.

## Project Structure

```text
ChurnGuard-AI/
├── app/
│   ├── routes/
│   ├── models/
│   ├── services/
│   ├── templates/
│   └── static/
├── data/
│   ├── raw/
│   └── processed/
├── ml/
│   └── model_artifacts/
├── tests/
├── app.py
├── config.py
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
```

## Notes

This project is designed as a production-style internship project and includes modular architecture, database integration, and ML workflows for real churn prediction.
