import numpy as np
import pandas as pd

# Define feature names explicitly
NUMERICAL_FEATURES = ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges']

CATEGORICAL_FEATURES = [
    'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
    'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]

ALL_INPUT_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess dataframe: drop customerID if present, convert TotalCharges to numeric, drop missing TotalCharges."""
    df_clean = df.copy()
    if 'customerID' in df_clean.columns:
        df_clean = df_clean.drop(columns=['customerID'])
    
    # Convert TotalCharges to numeric, coerce errors to NaN
    df_clean['TotalCharges'] = pd.to_numeric(df_clean['TotalCharges'], errors='coerce')
    
    # Ensure SeniorCitizen is numeric integer
    df_clean['SeniorCitizen'] = pd.to_numeric(df_clean['SeniorCitizen'], errors='coerce').fillna(0).astype(int)
    
    # Drop rows with NaN TotalCharges or missing values
    df_clean = df_clean.dropna(subset=['TotalCharges'])
    return df_clean


def get_risk_level(probability: float) -> str:
    """Categorize churn probability into risk levels."""
    if probability < 0.30:
        return 'Low Risk'
    elif probability < 0.70:
        return 'Medium Risk'
    else:
        return 'High Risk'


def get_retention_recommendations(risk_level: str, customer_data: dict) -> list:
    """Generate rule-based retention recommendations based on risk classification and customer features."""
    recommendations = []
    
    contract = customer_data.get('Contract', '')
    tech_support = customer_data.get('TechSupport', '')
    online_sec = customer_data.get('OnlineSecurity', '')
    payment = customer_data.get('PaymentMethod', '')
    internet = customer_data.get('InternetService', '')
    tenure = float(customer_data.get('tenure', 0))
    monthly_charges = float(customer_data.get('MonthlyCharges', 0))

    if risk_level == 'High Risk':
        recommendations.append("Immediate Action: Contact customer within 24 hours for direct retention outreach.")
        if contract == 'Month-to-month':
            recommendations.append("Offer 15% discount for upgrading from Month-to-month to a 1-year or 2-year contract.")
        if tech_support in ['No', 'No internet service']:
            recommendations.append("Provide 3 months of complimentary VIP Tech Support to resolve service issues.")
        if online_sec in ['No', 'No internet service']:
            recommendations.append("Bundle free Online Security and Device Protection features for 6 months.")
        if payment == 'Electronic check':
            recommendations.append("Offer a $5/month billing credit for switching to Automatic Bank Transfer / Credit Card.")
        if monthly_charges > 70:
            recommendations.append("Perform account review to offer custom loyalty package tailored to usage.")

    elif risk_level == 'Medium Risk':
        recommendations.append("Proactive Engagement: Include customer in active usage and satisfaction monitoring.")
        if contract == 'Month-to-month':
            recommendations.append("Promote long-term contract benefits with flexible cancellation options.")
        if internet == 'Fiber optic' and (online_sec == 'No' or tech_support == 'No'):
            recommendations.append("Recommend High-Speed Internet Security bundle with 20% discount.")
        if tenure < 12:
            recommendations.append("Send personalized onboarding check-in survey with small gratitude reward.")
        recommendations.append("Offer targeted promotional add-ons (e.g. streaming features or backup storage).")

    else: # Low Risk
        recommendations.append("Standard Engagement: Maintain regular service touchpoints and high customer satisfaction.")
        recommendations.append("Loyalty Program: Invite customer to join VIP Loyalty & Rewards program.")
        if tenure > 24:
            recommendations.append("Offer referral bonus rewards ($25 credit per friend referred).")
        recommendations.append("Explore cross-selling opportunities for premium upgrades or family plans.")

    return recommendations
