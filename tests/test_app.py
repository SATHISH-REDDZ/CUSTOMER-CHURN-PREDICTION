import os
import pytest
import sys

sys.path.append('.')
from app import app
from utils.database import init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    init_db()
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test home landing page HTTP 200."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Predict &amp; Prevent Customer Churn" in response.data or b"Predict & Prevent Customer Churn" in response.data


def test_about_route(client):
    """Test about page HTTP 200."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b"About Customer Churn Prediction System" in response.data


def test_dashboard_route(client):
    """Test dashboard route HTTP 200."""
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b"Business Intelligence Dashboard" in response.data


def test_analytics_route(client):
    """Test analytics route HTTP 200."""
    response = client.get('/analytics')
    assert response.status_code == 200
    assert b"Machine Learning Model Analytics" in response.data


def test_customers_history_route(client):
    """Test customers history table route HTTP 200."""
    response = client.get('/customers')
    assert response.status_code == 200
    assert b"Prediction History" in response.data


def test_export_csv_route(client):
    """Test CSV export route returns downloadable CSV file."""
    response = client.get('/export_csv')
    assert response.status_code == 200
    assert response.mimetype == 'text/csv'
    assert b"Customer ID,Gender" in response.data or b"ID,Customer ID" in response.data


def test_prediction_workflow(client):
    """Test full prediction submission via POST."""
    form_data = {
        'customer_id': 'TEST-9999',
        'gender': 'Female',
        'SeniorCitizen': '0',
        'Partner': 'Yes',
        'Dependents': 'No',
        'tenure': '12',
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'Fiber optic',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'Yes',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'Yes',
        'StreamingMovies': 'Yes',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check',
        'MonthlyCharges': '85.50',
        'TotalCharges': '1026.00'
    }
    
    response = client.post('/predict', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Customer Prediction Analysis" in response.data
    assert b"TEST-9999" in response.data
