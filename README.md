# Customer Churn Prediction System Using Machine Learning

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.3-green.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9.0-orange.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

## 📌 Project Overview

The **Customer Churn Prediction System** is a web-based Machine Learning and Business Intelligence application designed to predict whether a telecom customer is likely to churn (cancel or discontinue service). 

The system processes 19 customer features (demographics, services, contract terms, and billing details), calculates real-time churn probability, classifies customers into **Low, Medium, or High Risk** tiers, and generates targeted, rule-based **retention action plans**.

---

## 🚀 Main Features

- **Machine Learning Engine**:
  - Evaluates 4 classification models: **Logistic Regression, Random Forest, Decision Tree, and Gradient Boosting**.
  - Production model selected based on **ROC-AUC** metrics.
  - Automated `ColumnTransformer` pipeline with `StandardScaler` for numerical attributes and `OneHotEncoder` for categorical attributes saved as `model/churn_model.pkl`.
- **3-Tier Risk Categorization**:
  - **Low Risk**: Churn Probability < 30%
  - **Medium Risk**: 30% ≤ Churn Probability < 70%
  - **High Risk**: Churn Probability ≥ 70%
- **Rule-Based Retention Engine**: Generates targeted retention interventions (e.g., contract upgrade incentives, complimentary tech support, billing credits, account reviews).
- **Business Intelligence Dashboard**: Interactive visualizations powered by Chart.js displaying churn ratios, risk distributions, and contract trends.
- **Customer History Management**: SQLite database (`database/churn.db`) storing predictions with real-time search, risk level filtering, detail viewing, and deletion.
- **CSV Data Export**: 1-click export of prediction history for reporting or further analytics in Excel/PowerBI.
- **User Authentication**: Secure user registration and login with Werkzeug password hashing and session management.
- **Automated Pytest Suite**: Complete unit and integration test coverage for endpoints, model loading, probability boundaries, and risk logic.

---

## 🛠️ Technology Stack

| Category | Technology |
| :--- | :--- |
| **Programming Language** | Python 3.14 |
| **Web Framework** | Flask 3.1.3 |
| **Machine Learning** | Scikit-Learn 1.9.0, Joblib 1.5.3 |
| **Data Processing** | Pandas 3.0.3, NumPy 2.5.0 |
| **Database** | SQLite 3 |
| **Data Visualization** | Matplotlib 3.11.0, Seaborn 0.13.2, Chart.js |
| **Frontend UI** | HTML5, CSS3 Glassmorphism, JavaScript, Lucide Icons |
| **Testing** | Pytest 9.1.1, Pytest-Flask |
| **Security** | Werkzeug |

---

## 📁 Project Directory Structure

```
CUSTOMER CHURN PREDICTION/
│
├── app.py                         # Flask web application & routes
├── README.md                      # Comprehensive documentation
├── requirements.txt               # Dependencies list
├── LICENSE                        # MIT License
├── .gitignore                     # Git exclusion settings
│
├── dataset/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv   # 7,043 record Telco dataset
│
├── database/
│   └── churn.db                   # SQLite database
│
├── model/
│   ├── churn_model.pkl            # Saved sklearn preprocessing + ML pipeline
│   └── model_metrics.json         # Benchmark metrics & feature importances
│
├── notebooks/
│   └── customer_churn_analysis.ipynb  # EDA & ML analysis notebook
│
├── scripts/
│   ├── generate_dataset.py        # Dataset generation script
│   ├── train_model.py             # ML training & model evaluation script
│   └── create_database.py         # DB schema creation & seed script
│
├── static/
│   ├── css/
│   │   └── style.css              # Dark mode glassmorphism styles
│   └── js/
│       └── script.js              # Chart.js initialization & frontend logic
│
├── templates/
│   ├── base.html                  # Main layout shell
│   ├── index.html                 # Hero home landing page
│   ├── predict.html               # 19-feature input prediction form
│   ├── result.html                # Result analysis, gauge & retention checklist
│   ├── dashboard.html             # BI metrics dashboard & charts
│   ├── customers.html             # Customer history table & search filter
│   ├── analytics.html             # ML model benchmark & feature importances
│   ├── about.html                 # Architecture & methodology overview
│   ├── login.html                 # User login form
│   └── register.html              # User registration form
│
├── utils/
│   ├── preprocessing.py           # Feature definitions, cleaner & recommendation rules
│   └── database.py                # SQLite database helper functions
│
└── tests/
    ├── test_app.py                # Pytest Flask integration tests
    └── test_model.py              # Pytest model & risk classification unit tests
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites & Virtual Environment
```bash
# Clone repository
git clone <repo-url>
cd "CUSTOMER CHURN PREDICTION"

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Dataset & Train ML Model
```bash
# Generate Telco dataset
python scripts/generate_dataset.py

# Train models and export churn_model.pkl
python scripts/train_model.py
```

### 4. Initialize Database
```bash
python scripts/create_database.py
```
*Creates `database/churn.db` and populates default admin user (`admin` / `admin123`) and demo prediction records.*

### 5. Run Automated Tests
```bash
python -m pytest tests/ -v
```

### 6. Launch Flask Web Application
```bash
python app.py
```
Open your browser at `http://127.0.0.1:5000`.

---

## 📊 Model Evaluation Benchmark Results

| Algorithm | Accuracy | Precision | Recall | F1 Score | ROC-AUC | Production Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gradient Boosting** | **98.92%** | **98.29%** | **97.45%** | **97.87%** | **0.9991** | **Selected Best (ROC-AUC)** |
| **Decision Tree** | 98.63% | 97.44% | 97.17% | 97.30% | 0.9815 | Evaluated |
| **Random Forest** | 97.98% | 98.22% | 93.77% | 95.94% | 0.9986 | Evaluated |
| **Logistic Regression** | 96.25% | 94.93% | 90.08% | 92.44% | 0.9889 | Evaluated |

---

## 🎯 Conclusion

The Customer Churn Prediction System successfully demonstrates the use of Machine Learning to identify customers who are likely to leave a company. By analyzing historical customer data and training predictive models, the application provides accurate churn predictions that can help businesses improve customer retention. The project combines data preprocessing, exploratory data analysis, model evaluation, and a user-friendly Flask web interface to deliver an effective end-to-end solution.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
