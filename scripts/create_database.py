import os
import sys

sys.path.append('.')
from utils.database import init_db, register_user, save_prediction
import random

def seed_database():
    print("Initializing database schema...")
    init_db()
    
    # Register default admin user
    success, msg = register_user("admin", "admin123")
    if success:
        print("Default admin user created successfully (admin / admin123).")
    else:
        print("Admin user notice:", msg)
        
    print("Seeding sample customer predictions into database...")
    
    sample_customers = [
        {
            'customer_id': '7590-VHVEG', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'No',
            'tenure': 1, 'PhoneService': 'No', 'MultipleLines': 'No phone service', 'InternetService': 'DSL',
            'OnlineSecurity': 'No', 'OnlineBackup': 'Yes', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 29.85, 'TotalCharges': 29.85,
            'churn_pred': 1, 'churn_prob': 0.78, 'risk_level': 'High Risk',
            'recommendations': ['Immediate Action: Contact customer within 24 hours', 'Offer 15% discount for 1-year contract upgrade', 'Provide complimentary Tech Support']
        },
        {
            'customer_id': '5575-GNVDE', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 34, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'No', 'DeviceProtection': 'Yes', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'One year', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Mailed check', 'MonthlyCharges': 56.95, 'TotalCharges': 1889.50,
            'churn_pred': 0, 'churn_prob': 0.18, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Maintain regular service touchpoints', 'Invite customer to join VIP Loyalty Rewards program']
        },
        {
            'customer_id': '3668-QPYBK', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 2, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'Yes', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Mailed check', 'MonthlyCharges': 53.85, 'TotalCharges': 108.15,
            'churn_pred': 1, 'churn_prob': 0.64, 'risk_level': 'Medium Risk',
            'recommendations': ['Proactive Engagement: Monitor account usage', 'Promote long-term contract benefits']
        },
        {
            'customer_id': '7795-CFOCW', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 45, 'PhoneService': 'No', 'MultipleLines': 'No phone service', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'No', 'DeviceProtection': 'Yes', 'TechSupport': 'Yes',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'One year', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Bank transfer (automatic)', 'MonthlyCharges': 42.30, 'TotalCharges': 1840.75,
            'churn_pred': 0, 'churn_prob': 0.12, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Invite to VIP Rewards program']
        },
        {
            'customer_id': '9237-HQJCB', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 2, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 70.70, 'TotalCharges': 151.65,
            'churn_pred': 1, 'churn_prob': 0.85, 'risk_level': 'High Risk',
            'recommendations': ['Immediate Action: Contact customer within 24 hours', 'Offer 15% contract upgrade discount', 'Provide 3 months free Tech Support']
        },
        {
            'customer_id': '9305-CDSKC', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 8, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'Yes', 'TechSupport': 'No',
            'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 99.65, 'TotalCharges': 820.50,
            'churn_pred': 1, 'churn_prob': 0.82, 'risk_level': 'High Risk',
            'recommendations': ['Immediate Action: Contact customer within 24 hours', 'Perform custom account review for high monthly charges']
        },
        {
            'customer_id': '1452-KNGWZ', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 22, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No', 'OnlineBackup': 'Yes', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'Yes', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Credit card (automatic)', 'MonthlyCharges': 89.10, 'TotalCharges': 1949.40,
            'churn_pred': 1, 'churn_prob': 0.55, 'risk_level': 'Medium Risk',
            'recommendations': ['Proactive Engagement: Send personalized check-in survey', 'Recommend High-Speed Internet Security bundle']
        },
        {
            'customer_id': '6713-OKOMC', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 10, 'PhoneService': 'No', 'MultipleLines': 'No phone service', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'No', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Mailed check', 'MonthlyCharges': 29.75, 'TotalCharges': 301.90,
            'churn_pred': 0, 'churn_prob': 0.28, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Maintain regular service touchpoints']
        },
        {
            'customer_id': '7892-POOKP', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'No',
            'tenure': 28, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'Yes', 'TechSupport': 'Yes',
            'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 104.80, 'TotalCharges': 3046.05,
            'churn_pred': 1, 'churn_prob': 0.74, 'risk_level': 'High Risk',
            'recommendations': ['Immediate Action: Contact customer within 24 hours', 'Offer discount for upgrading contract']
        },
        {
            'customer_id': '6388-TABGU', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'Yes',
            'tenure': 62, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'Yes', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'One year', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Bank transfer (automatic)', 'MonthlyCharges': 56.15, 'TotalCharges': 3487.95,
            'churn_pred': 0, 'churn_prob': 0.08, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Invite to VIP Rewards program', 'Offer referral bonus rewards']
        }
    ]
    
    for c in sample_customers:
        save_prediction(
            user_id=1,
            data=c,
            churn_pred=c['churn_pred'],
            churn_prob=c['churn_prob'],
            risk_level=c['risk_level'],
            recommendations=c['recommendations']
        )
        
    print(f"Database seeded with {len(sample_customers)} sample prediction records.")

if __name__ == '__main__':
    seed_database()
