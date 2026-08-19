import os
import joblib
import pytest
import pandas as pd
from utils.preprocessing import get_risk_level, get_retention_recommendations, ALL_INPUT_FEATURES

MODEL_PATH = os.path.join('model', 'churn_model.pkl')


def test_model_file_exists():
    """Verify that trained model file exists."""
    assert os.path.exists(MODEL_PATH), "churn_model.pkl should exist in model directory."


def test_model_loading_and_prediction():
    """Verify that model loads and returns binary prediction and probability in range [0, 1]."""
    model = joblib.load(MODEL_PATH)
    
    sample_input = pd.DataFrame([{
        'SeniorCitizen': 0,
        'tenure': 1,
        'MonthlyCharges': 75.0,
        'TotalCharges': 75.0,
        'gender': 'Male',
        'Partner': 'No',
        'Dependents': 'No',
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'Fiber optic',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'No',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'No',
        'StreamingMovies': 'No',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check'
    }])[ALL_INPUT_FEATURES]

    prediction = model.predict(sample_input)[0]
    probabilities = model.predict_proba(sample_input)[0]

    assert prediction in [0, 1], f"Prediction should be binary 0 or 1, got {prediction}"
    assert 0.0 <= probabilities[0] <= 1.0, "Probability should be between 0 and 1"
    assert 0.0 <= probabilities[1] <= 1.0, "Probability should be between 0 and 1"
    assert abs(sum(probabilities) - 1.0) < 1e-5, "Probabilities should sum to 1.0"


def test_risk_level_classification():
    """Verify probability threshold risk categorization logic."""
    assert get_risk_level(0.15) == 'Low Risk'
    assert get_risk_level(0.29) == 'Low Risk'
    assert get_risk_level(0.30) == 'Medium Risk'
    assert get_risk_level(0.69) == 'Medium Risk'
    assert get_risk_level(0.70) == 'High Risk'
    assert get_risk_level(0.95) == 'High Risk'


def test_retention_recommendations_generation():
    """Verify rule-based retention recommendations logic."""
    high_risk_data = {
        'Contract': 'Month-to-month',
        'TechSupport': 'No',
        'PaymentMethod': 'Electronic check',
        'MonthlyCharges': 85.0
    }
    recs = get_retention_recommendations('High Risk', high_risk_data)
    assert len(recs) > 0
    assert any("Immediate Action" in r for r in recs)
    assert any("Month-to-month" in r or "contract" in r.lower() for r in recs)
