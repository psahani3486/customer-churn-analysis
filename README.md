# 📊 ChurnScope — Customer Churn Analysis Platform

A full-stack customer churn analysis platform with machine learning predictions, interactive visualizations, and a premium glassmorphism dashboard.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=flat-square&logo=flask)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange?style=flat-square)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-pink?style=flat-square)

---

## 🚀 Features

### 📈 Data Analytics
- **Overview Dashboard** — KPI cards with animated counters (total customers, churn rate, avg tenure, avg charges)
- **Churn Distribution** — Interactive doughnut chart showing churn vs. retained
- **Tenure Analysis** — Line chart showing churn rate across customer tenure groups
- **Contract & Billing** — Grouped bar charts for contract type, payment method analysis
- **Demographics** — Gender and senior citizen impact on churn
- **Service Analysis** — Internet service, phone service churn patterns

### 🤖 Machine Learning
- **3 Models Compared** — Random Forest, Gradient Boosting, Logistic Regression
- **Performance Metrics** — Accuracy, Precision, Recall, F1 Score, ROC AUC
- **Feature Importance** — Top 15 features driving churn predictions
- **Radar Comparison** — Visual model comparison across all metrics
- **Risk Segmentation** — High/Medium/Low risk customer categorization

### 🔮 Churn Predictor
- **Interactive Form** — Input customer profile details
- **Real-time Prediction** — ML-powered churn probability with risk level
- **Visual Gauge** — Animated probability gauge with color coding

### 🎨 Premium UI
- Dark mode with glassmorphism cards
- Animated gradient background orbs
- Responsive design (mobile/tablet/desktop)
- Smooth micro-animations and hover effects
- Inter font from Google Fonts

---

## 📂 Project Structure

```
customer-churn-analysis/
├── data/
│   ├── churn.csv                    # Telecom customer dataset (7,043 rows)
│   └── generate_data.py             # Dataset generation script
│
├── notebooks/
│   └── analysis.ipynb               # Jupyter notebook for exploration
│
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py        # Data cleaning, encoding, scaling
│   ├── eda.py                       # Exploratory data analysis
│   └── model.py                     # ML model training & evaluation
│
├── backend/
│   ├── app.py                       # Flask API server
│   ├── utils.py                     # Utility helpers
│   └── routes/
│       ├── __init__.py
│       ├── analytics.py             # EDA & stats endpoints
│       └── predictions.py           # Model & prediction endpoints
│
├── frontend/
│   ├── index.html                   # Dashboard page
│   ├── css/
│   │   └── style.css                # Glassmorphism dark theme
│   └── js/
│       ├── api.js                   # API communication layer
│       ├── charts.js                # Chart.js visualizations
│       └── app.js                   # Main application controller
│
├── dashboard/
│   └── (Power BI exports)
│
├── models/                          # Saved ML models (auto-generated)
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone & Install

```bash
cd customer-churn-analysis
pip install -r requirements.txt
```

### 2. Generate Dataset

```bash
python data/generate_data.py
```

### 3. Run the Server

```bash
python backend/app.py
```

### 4. Open Dashboard

Navigate to **http://localhost:5000** in your browser.

> **Note:** On first load, the backend trains ML models (~10-15 seconds). Subsequent loads use cached models.

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/overview` | Dataset overview statistics |
| `GET` | `/api/churn-distribution` | Churn vs retained counts |
| `GET` | `/api/demographics` | Demographic analysis |
| `GET` | `/api/services` | Service-level analysis |
| `GET` | `/api/contracts` | Contract & billing analysis |
| `GET` | `/api/tenure` | Tenure-based churn rates |
| `GET` | `/api/charges` | Charges analysis |
| `GET` | `/api/correlation` | Feature correlation matrix |
| `GET` | `/api/model-performance` | All model metrics |
| `GET` | `/api/feature-importance` | Top feature importances |
| `GET` | `/api/risk-segments` | Risk segmentation |
| `POST` | `/api/predict` | Predict churn for a customer |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Data Science** | Python, Pandas, NumPy, Scikit-learn |
| **Backend** | Flask, Flask-CORS |
| **Frontend** | HTML5, CSS3 (Glassmorphism), JavaScript |
| **Charts** | Chart.js 4.4 |
| **ML Models** | Random Forest, Gradient Boosting, Logistic Regression |
| **Typography** | Inter (Google Fonts) |

---

## 📊 Dataset

The synthetic telecom churn dataset contains **7,043 customers** with 21 features:

- **Demographics:** Gender, Senior Citizen, Partner, Dependents
- **Account:** Tenure, Contract, Billing, Payment Method
- **Services:** Phone, Internet, Security, Backup, Support, Streaming
- **Charges:** Monthly Charges, Total Charges
- **Target:** Churn (Yes/No)

---

## 📄 License

MIT License — Feel free to use and modify for your projects.
