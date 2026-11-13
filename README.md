# 🚀 ChurnGuard AI – Customer Churn Prediction & Retention Intelligence Platform

<p align="center">

  <img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-3.1.1-black?logo=flask" />
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange" />
  <img src="https://img.shields.io/badge/XGBoost-ML-red" />
  <img src="https://img.shields.io/badge/Database-SQLite-blue" />
  <img src="https://img.shields.io/badge/Status-Active-success" />

</p>

## 📌 Overview

**ChurnGuard AI** is a machine learning-powered customer churn prediction and retention intelligence platform designed to help businesses identify customers who are likely to discontinue their services.

Customer churn is one of the major challenges faced by subscription-based businesses. Losing existing customers can negatively impact revenue, customer lifetime value, and long-term business growth.

ChurnGuard AI addresses this challenge by combining machine learning, customer analytics, predictive modeling, and data-driven retention recommendations into a unified web application.

The platform allows users to analyze customer information, estimate churn probability, identify high-risk customers, compare machine learning models, and explore customer retention insights through an interactive dashboard.

Built using Python, Flask, Scikit-learn, XGBoost, SQLAlchemy, and Plotly, the application provides a complete end-to-end approach to customer churn analytics.

---

## 🎯 Project Objectives

- Predict the probability of customer churn using machine learning.
- Identify customers who are at high risk of leaving a business.
- Analyze customer behavior and subscription characteristics.
- Compare multiple machine learning algorithms.
- Provide actionable customer retention recommendations.
- Visualize business performance through an interactive dashboard.
- Maintain customer records and prediction history.
- Support individual and bulk customer churn predictions.

---

## ✨ Key Features

### 1. Individual Customer Prediction
- Enter customer information through an interactive form.
- Generate customer churn predictions.
- Calculate churn probability.
- Categorize customers according to their predicted risk level.

### 2. Bulk Customer Prediction
- Upload customer datasets using CSV files.
- Process multiple customer records.
- Generate churn predictions for multiple customers.
- Simplify large-scale customer risk analysis.

### 3. Interactive Analytics Dashboard
- View important customer churn metrics.
- Monitor customer distribution and churn patterns.
- Analyze customer subscription characteristics.
- Explore business insights through interactive visualizations.

### 4. Machine Learning Model Comparison
- Train and evaluate multiple machine learning algorithms.
- Compare model performance.
- Analyze predictive performance using evaluation metrics.
- Support data-driven model selection.

### 5. Customer Risk Classification
Identify customers according to their predicted churn probability.

- **Low Risk:** Customers with a relatively low predicted churn probability.
- **Medium Risk:** Customers requiring additional attention.
- **High Risk:** Customers with a relatively high predicted churn probability.

*Risk categories represent model-based estimates and should not be interpreted as guaranteed customer behavior.*

### 6. Retention Recommendation System
- Generate retention recommendations based on customer attributes.
- Identify customer characteristics associated with churn risk.
- Support proactive customer engagement strategies.

### 7. User Authentication
- User registration.
- Secure login system.
- Password hashing.
- Session-based authentication.

### 8. Prediction History
- Store customer information.
- Maintain prediction records.
- Track predicted churn probabilities.
- Store model version information.

---

## 🧠 Machine Learning Approach

ChurnGuard AI follows an end-to-end machine learning workflow.

**Machine Learning Pipeline:**

1. Data Collection
2. Data Preprocessing
3. Exploratory Data Analysis (EDA)
4. Feature Preparation
5. Model Training
6. Model Evaluation
7. Model Comparison
8. Churn Risk Prediction
9. Prediction Storage
10. Customer Retention Insights

### Machine Learning Algorithms

The project dependencies include support for the following machine learning technologies:

| Algorithm / Technology | Purpose |
|---|---|
| Logistic Regression | Classification and baseline prediction |
| Random Forest | Ensemble-based classification |
| Support Vector Machine (SVM) | Classification using decision boundaries |
| XGBoost | Gradient boosting-based classification |
| Scikit-learn | Model development and evaluation |
| SHAP | Model explainability and feature contributions |

The final model selection should be based on actual evaluation results rather than assuming that one algorithm performs best.

### Model Evaluation Metrics

The following metrics can be used to evaluate classification performance:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- ROC-AUC Score

---

## 📊 Dataset

The project uses a customer churn dataset containing customer demographic, account, service, and billing information.

The dataset includes features such as:

| Feature | Description |
|---|---|
| customerID | Unique customer identifier |
| gender | Customer gender |
| SeniorCitizen | Senior citizen indicator |
| Partner | Partner status |
| Dependents | Dependent status |
| tenure | Number of months with the company |
| PhoneService | Phone service subscription |
| MultipleLines | Multiple phone lines status |
| InternetService | Internet service type |
| OnlineSecurity | Online security subscription |
| OnlineBackup | Online backup subscription |
| DeviceProtection | Device protection subscription |
| TechSupport | Technical support subscription |
| StreamingTV | Streaming TV subscription |
| StreamingMovies | Streaming movies subscription |
| Contract | Customer contract type |
| PaperlessBilling | Paperless billing status |
| PaymentMethod | Customer payment method |
| MonthlyCharges | Monthly subscription charges |
| TotalCharges | Total customer charges |
| Churn | Target variable |

**Target Variable:**
- Yes – Customer discontinued the service.
- No – Customer continued the service.

The uploaded dataset contains 300 customer records and 21 columns.

---

## 🛠️ Technology Stack

### Backend Development
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF

### Machine Learning & Data Science
- Scikit-learn
- XGBoost
- Pandas
- NumPy
- SHAP
- Joblib

### Data Visualization
- Plotly
- Matplotlib
- Seaborn

### Database
- SQLite
- SQLAlchemy ORM

### Development Tools
- Visual Studio Code
- Git
- GitHub
- Python Virtual Environment

---

## 🏗️ Project Architecture

```text
ChurnGuard-AI/
│
├── app/
│   ├── routes/
│   │   ├── Authentication & Application Routes
│   │
│   ├── models/
│   │   ├── Database Models
│   │
│   ├── services/
│   │   ├── Business Logic
│   │
│   ├── templates/
│   │   ├── HTML Templates
│   │
│   └── static/
│       ├── CSS
│       ├── JavaScript
│       └── Assets
│
├── data/
│   ├── raw/
│   └── processed/
│
├── ml/
│   └── model_artifacts/
│
├── tests/
│
├── app.py
├── config.py
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
```

---

## ⚙️ Installation & Setup

Follow these steps to run ChurnGuard AI locally.

### Prerequisites

Make sure you have installed:

- Python 3.12 or later
- Git
- Visual Studio Code
- pip

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ChurnGuard-AI.git
```

### Step 2: Navigate to Project Directory

```bash
cd ChurnGuard-AI
```

### Step 3: Create a Virtual Environment

**Windows:**

```bash
py -3.12 -m venv .venv
```

### Step 4: Activate Virtual Environment

```bash
.venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
python run.py
```

### Step 7: Open the Application

Open your browser and navigate to:

```text
http://127.0.0.1:5000/login
```

The Flask application will start locally.

The first local run initializes the SQLite database and trains the machine learning model if the required model artifacts are missing.

---

## 🔐 Application Access

The existing development configuration documents the following initial credentials:

```text
Username: admin
Password: admin123
```

**Security Notice:** These are development credentials. Change or remove the default account before deploying the application or exposing it to a network.

---

## 📈 Expected Business Impact

ChurnGuard AI is designed to support businesses in:

- Identifying potentially lost customers.
- Understanding customer churn patterns.
- Improving customer retention strategies.
- Making data-driven business decisions.
- Prioritizing high-risk customer segments.
- Reducing manual customer analysis efforts.

The platform provides predictive insights to support business decision-making; actual retention and revenue improvements require validation in real business environments.

---

## 🔮 Future Enhancements

Potential future improvements include:

- Real-time churn prediction.
- Advanced customer segmentation.
- Automated email-based retention campaigns.
- Advanced SHAP explainability dashboard.
- Deep learning-based churn prediction.
- Cloud deployment and API integration.
- Advanced customer lifetime value prediction.
- Automated model retraining.
- Real-time business intelligence reporting.

---

## ⚠️ Important Disclaimer

ChurnGuard AI is an educational and analytical machine learning project.

Predictions are estimates generated from historical customer data and should not be treated as guaranteed outcomes. Business decisions should consider additional customer information and human judgment.

---

## 👨‍💻 Author

**Armaan Singh**

B.Tech – Artificial Intelligence & Machine Learning

Dronacharya College of Engineering, Gurugram

### Connect With Me

- LinkedIn: https://www.linkedin.com/in/armaan-singh-511a78323/
- GitHub: https://github.com/YOUR_USERNAME

---

## ⭐ Support

If you find this project interesting or useful:

- Give this repository a ⭐ Star.
- Fork the repository.
- Share your suggestions and feedback.
- Contribute to improving the project.

**Built with Python, Machine Learning, and a vision to make customer retention smarter.**

# ChurnGuard AI 🚀
