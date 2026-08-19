# Customer Churn Prediction System Using Machine Learning

A complete web-based **Customer Churn Prediction System** developed using **Python, Flask, Pandas, NumPy, Scikit-learn, SQLite, HTML5, CSS3, JavaScript, Matplotlib, Seaborn, Chart.js, Pytest, and Joblib**.

The system is designed to analyze telecom customer information, predict the probability that a customer may leave the service, classify customers according to their churn risk, and provide retention recommendations. The project combines **Machine Learning, Data Analysis, Web Development, Database Management, Data Visualization, Authentication, and Automated Testing** into a single end-to-end application.


![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.3-green.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9.0-orange.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

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

# 📌 Project Overview

Customer churn is a major business challenge for telecom and subscription-based organizations. Customer churn occurs when an existing customer stops using a company's products or services. Losing existing customers can affect business revenue and may also increase the cost of acquiring new customers.

The **Customer Churn Prediction System** is developed to help businesses identify customers who have a higher probability of leaving their service. Instead of waiting until a customer actually leaves, the system uses historical customer information and Machine Learning techniques to identify potential churners in advance.

The application processes **19 customer features** related to customer demographics, subscribed services, contract information, billing details, and service usage. These features are passed through a trained Machine Learning pipeline that performs the required preprocessing and generates a churn prediction.

The system calculates a **churn probability** and converts the prediction into one of three risk categories:

* 🟢 **Low Risk** – Churn probability below 30%
* 🟡 **Medium Risk** – Churn probability from 30% to below 70%
* 🔴 **High Risk** – Churn probability of 70% or above

In addition to prediction, the application provides rule-based retention recommendations. These recommendations can help businesses decide what type of action may be appropriate for customers who have a higher risk of leaving.

The project is implemented as a Flask-based web application. Users can register and log in, enter customer information, generate predictions, view results, access customer history, analyze business metrics, and export prediction records.

---

# 🎯 Project Objectives

The primary objective of this project is to develop an intelligent system that can predict customer churn using Machine Learning and present the results through an easy-to-use web interface.

The major objectives are:

* Predict whether a telecom customer is likely to churn.
* Calculate the probability of customer churn.
* Classify customers according to their churn risk.
* Analyze historical telecom customer information.
* Perform data cleaning and preprocessing.
* Transform numerical and categorical features into Machine Learning-ready data.
* Perform Exploratory Data Analysis.
* Train multiple Machine Learning classification algorithms.
* Compare the performance of different models.
* Select the most suitable production model.
* Save the trained Machine Learning pipeline.
* Provide real-time customer churn predictions.
* Generate retention recommendations for at-risk customers.
* Store prediction history using SQLite.
* Provide customer search and filtering functionality.
* Display business intelligence information using interactive charts.
* Export customer prediction history as CSV.
* Provide user registration and login functionality.
* Implement password hashing and session management.
* Test important application and Machine Learning components using Pytest.

---

# 🚀 Main Features

## 1. Machine Learning Prediction

The main functionality of the application is Machine Learning-based customer churn prediction.

The system evaluates four classification algorithms:

* Logistic Regression
* Random Forest
* Decision Tree
* Gradient Boosting

Each model is trained using the processed customer dataset and evaluated using multiple performance metrics.

The system compares the models and selects the best-performing model based on the documented ROC-AUC results.

The trained preprocessing and Machine Learning pipeline is stored in:

```text
model/churn_model.pkl
```

The saved pipeline allows the Flask application to load the trained model and use it for real-time predictions without retraining the model every time a customer enters information.

---

## 2. Automated Data Preprocessing

Raw customer data contains both numerical and categorical information. Machine Learning algorithms require data to be represented in a suitable numerical format.

The project uses a Scikit-learn `ColumnTransformer` pipeline to perform preprocessing automatically.

### Numerical Features

Numerical features are processed using:

```text
StandardScaler
```

StandardScaler standardizes numerical values so that features with different ranges can be processed consistently.

### Categorical Features

Categorical features are transformed using:

```text
OneHotEncoder
```

OneHotEncoder converts categorical values into numerical representations suitable for Machine Learning algorithms.

The preprocessing operations are integrated with the Machine Learning model pipeline. This ensures that the same transformation process is applied during both model training and real-time prediction.

---

# 3. Three-Tier Churn Risk Classification

The system converts the predicted churn probability into a simple risk category.

| Risk Level     |    Churn Probability |
| -------------- | -------------------: |
| 🟢 Low Risk    |        Less than 30% |
| 🟡 Medium Risk | 30% to less than 70% |
| 🔴 High Risk   |        70% or higher |

This classification makes Machine Learning predictions easier for business users to understand.

For example, if a customer receives a churn probability of 82%, the system identifies the customer as:

```text
Churn Probability: 82%
Risk Level: HIGH
```

The business can then prioritize this customer for retention activities.

---

# 4. Retention Recommendation Engine

Prediction alone is not always enough for a business. Once a potentially high-risk customer has been identified, the business needs to decide what action should be taken.

The project therefore includes a rule-based retention recommendation engine.

Depending on customer information and risk level, the system can provide recommendations such as:

* Contract upgrade incentives
* Complimentary technical support
* Billing credits
* Account reviews
* Customer service follow-up
* Retention offers
* Personalized customer engagement

The purpose of this feature is to convert Machine Learning predictions into actionable business information.

The overall process becomes:

```text
Customer Information
        ↓
Churn Prediction
        ↓
Risk Classification
        ↓
Retention Recommendation
        ↓
Business Action
```

---

# 5. Business Intelligence Dashboard

The project includes an interactive Business Intelligence dashboard that allows users to understand customer churn information through visualizations.

The dashboard provides information such as:

* Overall churn ratio
* Customer prediction statistics
* Risk distribution
* Contract-related trends
* Prediction information
* Interactive business charts

The dashboard uses **Chart.js** to provide interactive web-based visualizations.

This makes it easier for business users to understand customer churn patterns instead of depending only on raw numerical results.

---

# 6. Customer History Management

Prediction results are stored in an SQLite database.

Database:

```text
database/churn.db
```

The customer history functionality provides:

* Prediction history
* Customer search
* Risk-level filtering
* Prediction detail viewing
* Record deletion
* CSV export

This allows users to maintain a history of predictions instead of losing the results after a prediction is completed.

The stored information can also be used for further analysis and reporting.

---

# 7. CSV Export

The application provides a CSV export functionality for customer prediction records.

Users can export prediction information and use the generated CSV file for:

* Microsoft Excel
* Power BI
* Business reporting
* Further data analysis
* Record keeping

This feature makes the application more useful for organizations that already use external reporting and analytics tools.

---

# 8. User Authentication

The system includes user authentication functionality.

Users can:

* Register an account
* Log in to the application
* Access protected application functionality
* Maintain an authenticated session

The application uses **Werkzeug** for password hashing and session-related security functionality.

Authentication provides controlled access to the application's prediction and customer-management features.

---

# 9. Automated Testing

Testing is included to improve application reliability.

The project uses:

* **Pytest**
* **Pytest-Flask**

Testing covers important areas such as:

* Flask application routes
* Application integration
* Model loading
* Prediction functionality
* Churn probability boundaries
* Risk classification
* Machine Learning components

Tests can be executed using:

```bash
python -m pytest tests/ -v
```

---

# 🧠 Machine Learning Workflow

The complete Machine Learning workflow is:

```text
Customer Dataset
       ↓
Data Cleaning
       ↓
Data Preprocessing
       ↓
Feature Transformation
       ↓
Exploratory Data Analysis
       ↓
Train Multiple ML Models
       ↓
Model Evaluation
       ↓
Best Model Selection
       ↓
Save Trained Pipeline
       ↓
Flask Web Application
       ↓
Customer Input
       ↓
Churn Probability
       ↓
Risk Classification
       ↓
Retention Recommendation
       ↓
Store Prediction
       ↓
Dashboard / Analytics
```

The workflow ensures that the project covers the complete lifecycle of a Machine Learning application, from raw data preparation to deployment through a web interface.

---

# 📊 Dataset

The project uses the telecom customer churn dataset:

```text
WA_Fn-UseC_-Telco-Customer-Churn.csv
```

The dataset contains:

**7,043 customer records**

The dataset provides customer information that can be used to identify patterns associated with customer churn.

Important customer attributes include:

* Customer tenure
* Gender
* Senior citizen status
* Partner
* Dependents
* Phone service
* Internet service
* Online security
* Online backup
* Device protection
* Technical support
* Streaming services
* Contract
* Paperless billing
* Payment method
* Monthly charges
* Total charges
* Other telecom service information

These features provide information about customer demographics, service usage, contract characteristics, and billing behavior.

---

# 🔬 Exploratory Data Analysis

Exploratory Data Analysis is performed before Machine Learning model training.

The purpose of EDA is to understand the dataset, identify important patterns, inspect customer behavior, and understand the relationship between customer attributes and churn.

The analysis includes:

* Dataset inspection
* Customer distribution
* Churn distribution
* Numerical feature analysis
* Categorical feature analysis
* Contract analysis
* Tenure analysis
* Monthly charge analysis
* Total charge analysis
* Service usage analysis
* Customer behavior patterns

The project includes a Jupyter Notebook:

```text
notebooks/customer_churn_analysis.ipynb
```

The notebook is used for data analysis and Machine Learning experimentation.

Visualization is performed using:

* Matplotlib
* Seaborn

These libraries help create graphs and charts for understanding customer behavior and data distribution.

---

# 🤖 Machine Learning Models

The project evaluates four Machine Learning classification algorithms.

## 1. Logistic Regression

Logistic Regression is used as one of the classification models and provides a baseline for comparison.

It estimates the probability that a customer belongs to the churn class.

### Advantages

* Simple
* Fast
* Easy to interpret
* Suitable for binary classification
* Provides probability-based predictions

---

## 2. Random Forest

Random Forest is an ensemble Machine Learning algorithm that combines multiple decision trees.

Instead of relying on a single decision tree, Random Forest combines the predictions of multiple trees to produce a more stable result.

### Advantages

* Good generalization
* Handles complex relationships
* Reduces dependence on a single tree
* Suitable for classification problems

---

## 3. Decision Tree

Decision Tree creates a tree-like decision structure based on customer features.

It repeatedly divides the data based on feature conditions until it reaches classification decisions.

### Advantages

* Easy to understand
* Easy to visualize
* Useful for interpreting decision patterns
* Can model nonlinear relationships

---

## 4. Gradient Boosting

Gradient Boosting is an ensemble learning algorithm that builds models sequentially.

Each new model attempts to correct errors made by previous models. This allows the final model to capture complex patterns within the customer data.

In this project, Gradient Boosting achieved the highest documented ROC-AUC score and was selected as the production model.

---

# 📈 Model Evaluation

The Machine Learning models are evaluated using multiple performance metrics.

The project uses:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC

These metrics provide different perspectives on model performance.

### Accuracy

Measures the overall percentage of correctly classified predictions.

### Precision

Measures how many customers predicted as churners were actually churners.

### Recall

Measures how many actual churners were correctly identified.

### F1 Score

Provides a balance between precision and recall.

### ROC-AUC

Measures the model's ability to distinguish between churn and non-churn customers across different classification thresholds.

---

# 📊 Benchmark Results

| Algorithm           | Accuracy | Precision | Recall | F1 Score | ROC-AUC | Status     |
| ------------------- | -------: | --------: | -----: | -------: | ------: | ---------- |
| Gradient Boosting   |   98.92% |    98.29% | 97.45% |   97.87% |  0.9991 | ⭐ Selected |
| Decision Tree       |   98.63% |    97.44% | 97.17% |   97.30% |  0.9815 | Evaluated  |
| Random Forest       |   97.98% |    98.22% | 93.77% |   95.94% |  0.9986 | Evaluated  |
| Logistic Regression |   96.25% |    94.93% | 90.08% |   92.44% |  0.9889 | Evaluated  |

According to the documented benchmark results, **Gradient Boosting** is selected as the production model because it achieved the highest ROC-AUC score:

```text
ROC-AUC = 0.9991
```

The selected model is stored as part of the trained Machine Learning pipeline.

---

# 🔄 Prediction Process

The prediction process is designed to be simple for the end user.

### Step 1 – User Login

The user logs into the application using their registered account.

### Step 2 – Open Prediction Page

The user opens the customer prediction page.

### Step 3 – Enter Customer Information

The user provides the required customer information using the 19-feature input form.

### Step 4 – Input Validation

The application validates and processes the submitted information.

### Step 5 – Data Preprocessing

The trained preprocessing pipeline transforms the customer information.

### Step 6 – Machine Learning Prediction

The trained model processes the transformed customer information.

### Step 7 – Calculate Churn Probability

The model generates the probability that the customer may churn.

### Step 8 – Risk Classification

The probability is converted into:

* Low Risk
* Medium Risk
* High Risk

### Step 9 – Display Result

The prediction result is displayed to the user.

### Step 10 – Generate Recommendation

The system provides retention recommendations based on the customer and risk level.

### Step 11 – Store Prediction

The prediction is saved into the SQLite database.

### Step 12 – Analytics

The prediction becomes available for customer history, dashboard statistics, and analytics.

---

# 🖥️ Web Application

The Flask application provides multiple pages and functionalities.

## Home Page

The Home Page introduces the Customer Churn Prediction System and provides information about the application's purpose and capabilities.

---

## Prediction Page

The Prediction Page provides the input form where users enter customer information.

The form contains the required **19 customer features** used by the Machine Learning pipeline.

---

## Result Page

After prediction, the Result Page displays:

* Churn probability
* Risk level
* Prediction result
* Visual gauge
* Retention recommendations

This provides an easy-to-understand representation of the Machine Learning result.

---

## Dashboard

The Dashboard provides business-level information through:

* Churn statistics
* Risk distribution
* Contract trends
* Interactive charts
* Business metrics

---

## Customers Page

The Customers Page manages prediction history.

It provides:

* Customer prediction history
* Search
* Risk filtering
* Record details
* Delete functionality
* CSV export

---

## Analytics Page

The Analytics Page provides:

* Machine Learning model benchmark results
* Model performance
* Feature importance information
* Analytical information

---

## About Page

The About Page provides information about:

* The project
* System architecture
* Methodology
* Machine Learning approach

---

## Authentication Pages

The application provides:

* Registration
* Login

These pages allow users to create accounts and access the application through authentication.

---

# 🗄️ Database

The application uses **SQLite** as its database system.

Database:

```text
database/churn.db
```

SQLite is lightweight and suitable for this type of standalone Flask application.

The database is used to store:

* User information
* Customer prediction records
* Churn probability
* Risk levels
* Prediction history
* Related application information

Database helper functionality is implemented in:

```text
utils/database.py
```

Database creation and initialization are handled by:

```text
scripts/create_database.py
```

---

# 📁 Project Structure

```text
CUSTOMER CHURN PREDICTION/
│
├── app.py
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── dataset/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
│
├── database/
│   └── churn.db
│
├── model/
│   ├── churn_model.pkl
│   └── model_metrics.json
│
├── notebooks/
│   └── customer_churn_analysis.ipynb
│
├── scripts/
│   ├── generate_dataset.py
│   ├── train_model.py
│   └── create_database.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── predict.html
│   ├── result.html
│   ├── dashboard.html
│   ├── customers.html
│   ├── analytics.html
│   ├── about.html
│   ├── login.html
│   └── register.html
│
├── utils/
│   ├── preprocessing.py
│   └── database.py
│
└── tests/
    ├── test_app.py
    └── test_model.py
```

---

# 🛠️ Technology Stack

| Category             | Technology                    |
| -------------------- | ----------------------------- |
| Programming Language | Python 3.14                   |
| Web Framework        | Flask 3.1.3                   |
| Machine Learning     | Scikit-learn 1.9.0            |
| Model Serialization  | Joblib 1.5.3                  |
| Data Processing      | Pandas 3.0.3                  |
| Numerical Computing  | NumPy 2.5.0                   |
| Database             | SQLite 3                      |
| Visualization        | Matplotlib, Seaborn, Chart.js |
| Frontend             | HTML5, CSS3, JavaScript       |
| UI Design            | Glassmorphism / Dark Mode     |
| Icons                | Lucide Icons                  |
| Testing              | Pytest, Pytest-Flask          |
| Security             | Werkzeug                      |
| Version Control      | Git & GitHub                  |

---

# ⚡ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/SATHISH-REDDZ/CUSTOMER-CHURN-PREDICTION.git
```

## 2. Navigate to the Project

```bash
cd CUSTOMER-CHURN-PREDICTION
```

## 3. Create a Virtual Environment

```bash
python -m venv venv
```

## 4. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## Generate Dataset

```bash
python scripts/generate_dataset.py
```

This prepares the required customer dataset for the application.

## Train Machine Learning Models

```bash
python scripts/train_model.py
```

This process trains and evaluates the Machine Learning models and generates the trained model pipeline.

## Create the Database

```bash
python scripts/create_database.py
```

This initializes:

```text
database/churn.db
```

## Run Tests

```bash
python -m pytest tests/ -v
```

## Start the Flask Application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

in a web browser.

---

# 🧪 Testing

Automated testing is included to verify important parts of the application.

Run the complete test suite using:

```bash
python -m pytest tests/ -v
```

The testing system covers areas including:

* Flask application routes
* Application integration
* Model loading
* Prediction functionality
* Probability boundaries
* Risk classification
* Machine Learning components

Automated testing helps identify problems during development and provides additional confidence in the application's functionality.

---

# 📊 Business Use Case

The system is designed around a practical customer retention scenario.

For example, suppose a customer provides information indicating that they have a high probability of leaving.

The system may produce:

```text
Customer Data
      ↓
Machine Learning Prediction
      ↓
Churn Probability: 82%
      ↓
Risk Level: HIGH
      ↓
Retention Recommendation
      ↓
Customer Support / Special Offer
```

Instead of waiting until the customer terminates the service, the organization can use the prediction to take proactive action.

Potential business actions can include:

* Contacting the customer
* Offering an incentive
* Reviewing the customer's plan
* Providing technical support
* Offering a contract upgrade
* Providing a billing-related benefit

This demonstrates how Machine Learning can be integrated with business decision-making.

---

# 💡 Advantages

## Early Churn Detection

The system identifies customers who have a higher probability of leaving.

## Automated Machine Learning

Predictions are generated automatically using the trained Machine Learning pipeline.

## Multiple Model Comparison

Four different classification algorithms are evaluated before selecting the production model.

## Probability-Based Prediction

The application provides a churn probability rather than only returning a simple yes/no result.

## Risk Categorization

Customers are classified into three understandable risk levels.

## Retention Recommendations

The system provides possible actions for customers identified as being at risk.

## Interactive Dashboard

Users can understand customer churn patterns through visualizations.

## Prediction History

Previous predictions can be stored and reviewed.

## CSV Export

Prediction information can be exported for further analysis.

## Authentication

User registration and login provide controlled access.

## Automated Testing

Pytest provides automated validation of important application functionality.

---

# 🌍 Real-World Applications

The customer churn prediction approach can be applied to multiple industries.

### Telecom

Identify customers who may cancel their mobile or internet services.

### Internet Service Providers

Predict customers who may switch to another provider.

### Banking

Identify customers who may close accounts or move to another bank.

### Insurance

Predict customers who may not renew their insurance policies.

### E-commerce

Identify customers who are becoming inactive.

### Subscription Services

Predict subscribers who may cancel their subscriptions.

### SaaS Platforms

Identify business customers who may stop renewing software subscriptions.

### Streaming Services

Predict users who may cancel their memberships.

### Financial Services

Identify customers with a high likelihood of discontinuing a service.

The underlying Machine Learning architecture can be adapted by changing the dataset, customer features, model, and business rules.

---

# 🔮 Future Enhancements

The current system can be extended with several advanced capabilities.

## Real-Time Customer Data Integration

Connect the application directly to real-time customer databases or APIs.

## REST API

Provide a REST API so external applications can send customer data and receive churn predictions.

## Cloud Deployment

Deploy the application to cloud platforms for remote access and scalability.

## Docker Support

Containerize the application using Docker for easier deployment.

## CI/CD Integration

Automate testing and deployment using a Continuous Integration and Continuous Deployment pipeline.

## Explainable AI

Integrate SHAP or similar techniques to explain why a customer is classified as high risk.

## Automated Model Retraining

Automatically retrain the Machine Learning model when new customer data becomes available.

## Data Drift Detection

Monitor changes in customer data distributions that could affect model performance.

## Model Monitoring

Track production model performance over time.

## Email Notifications

Automatically notify customer support teams when high-risk customers are detected.

## SMS Alerts

Send retention alerts for customers with high churn probabilities.

## Advanced Customer Segmentation

Group customers according to their characteristics and behavior before applying targeted retention strategies.

## Power BI Integration

Connect prediction data directly with Power BI for advanced business reporting.

## Role-Based Access Control

Introduce different application roles such as:

* Administrator
* Manager
* Analyst
* Customer Support User

## Advanced Recommendation System

Replace or enhance the current rule-based recommendation engine with a Machine Learning-based recommendation system.

---

# 📌 Key Project Highlights

* Complete web-based Machine Learning application
* Telecom customer churn prediction
* 19 customer input features
* 7,043 customer records
* Four Machine Learning classification algorithms
* Logistic Regression
* Random Forest
* Decision Tree
* Gradient Boosting
* Gradient Boosting selected as production model
* Documented ROC-AUC of 0.9991
* Three-level churn risk classification
* Rule-based retention recommendations
* Automated preprocessing pipeline
* SQLite prediction history
* Interactive Business Intelligence dashboard
* Chart.js visualizations
* CSV export
* User registration
* User login
* Password hashing
* Session management
* Automated Pytest testing
* Flask backend
* HTML/CSS/JavaScript frontend
* Git and GitHub version control

---

# 🎓 Skills Demonstrated

This project demonstrates practical skills in:

### Programming

* Python
* JavaScript
* SQL
* HTML
* CSS

### Machine Learning

* Supervised Learning
* Binary Classification
* Logistic Regression
* Decision Trees
* Random Forest
* Gradient Boosting
* Model Evaluation
* Probability Prediction
* Risk Classification
* Scikit-learn Pipelines

### Data Science

* Pandas
* NumPy
* Data Cleaning
* Data Preprocessing
* Exploratory Data Analysis
* Feature Transformation
* Data Visualization

### Web Development

* Flask
* HTML5
* CSS3
* JavaScript
* Responsive Web Design
* Dashboard Development

### Database

* SQLite
* SQL
* Database Management
* CRUD Operations

### Visualization

* Matplotlib
* Seaborn
* Chart.js

### Testing

* Pytest
* Pytest-Flask
* Application Testing
* Machine Learning Testing

### Security

* Password Hashing
* Authentication
* Session Management

### Development Tools

* Git
* GitHub
* Jupyter Notebook
* Python Virtual Environment

---

# 🏆 Conclusion

The **Customer Churn Prediction System** is an end-to-end Machine Learning web application developed to help businesses identify customers who may discontinue their services.

The project combines multiple areas of software development and Machine Learning, including data preprocessing, exploratory data analysis, supervised learning, model evaluation, real-time prediction, risk classification, retention recommendations, database management, dashboard visualization, authentication, automated testing, and version control.

The system evaluates four Machine Learning algorithms: **Logistic Regression, Random Forest, Decision Tree, and Gradient Boosting**. Based on the documented benchmark results, Gradient Boosting is selected as the production model with a reported ROC-AUC score of **0.9991**.

The application provides a complete workflow from customer data input to actionable business recommendations:

```text
Customer Information
        ↓
Data Preprocessing
        ↓
Machine Learning Model
        ↓
Churn Probability
        ↓
Risk Classification
        ↓
Retention Recommendation
        ↓
Database Storage
        ↓
Dashboard / Analytics
```

By converting customer information into a probability-based churn prediction and an understandable risk category, the system can help organizations identify potentially at-risk customers and take proactive retention measures.

The project demonstrates practical implementation of **Python, Flask, Scikit-learn, Pandas, NumPy, SQLite, HTML5, CSS3, JavaScript, Matplotlib, Seaborn, Chart.js, Joblib, Pytest, Git, and GitHub**.

Overall, the project provides a complete foundation for developing intelligent customer retention systems and can be further extended with cloud deployment, explainable AI, automated retraining, real-time data integration, advanced recommendations, and production monitoring.

---



