import os
import sys

sys.path.append('.')
from utils.database import init_db, register_user, save_prediction, get_db_connection

def seed_database():
    print("Initializing database schema...")
    init_db()
    
    # Register default admin user
    success, msg = register_user("admin", "admin123")
    if success:
        print("Default admin user created successfully (admin / admin123).")
    else:
        print("Admin user notice:", msg)

    # Clear existing sample predictions to maintain exact count of 25 records
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()
        
    print("Seeding 25 customer churn dataset records into database...")
    
    sample_customers = [
        # 1. High Risk
        {
            'customer_id': '7590-VHVEG', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'No',
            'tenure': 1, 'PhoneService': 'No', 'MultipleLines': 'No phone service', 'InternetService': 'DSL',
            'OnlineSecurity': 'No', 'OnlineBackup': 'Yes', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 29.85, 'TotalCharges': 29.85,
            'churn_pred': 1, 'churn_prob': 0.78, 'risk_level': 'High Risk',
            'recommendations': ['Immediate Action: Contact customer within 24 hours', 'Offer 15% discount for 1-year contract upgrade', 'Provide complimentary Tech Support']
        },
        # 2. Low Risk
        {
            'customer_id': '5575-GNVDE', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 34, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'No', 'DeviceProtection': 'Yes', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'One year', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Mailed check', 'MonthlyCharges': 56.95, 'TotalCharges': 1889.50,
            'churn_pred': 0, 'churn_prob': 0.18, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Maintain regular service touchpoints', 'Invite customer to join VIP Loyalty Rewards program']
        },
        # 3. Medium Risk
        {
            'customer_id': '3668-QPYBK', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 2, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'Yes', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Mailed check', 'MonthlyCharges': 53.85, 'TotalCharges': 108.15,
            'churn_pred': 1, 'churn_prob': 0.64, 'risk_level': 'Medium Risk',
            'recommendations': ['Proactive Engagement: Monitor account usage', 'Promote long-term contract benefits']
        },
        # 4. Low Risk
        {
            'customer_id': '7795-CFOCW', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 45, 'PhoneService': 'No', 'MultipleLines': 'No phone service', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'No', 'DeviceProtection': 'Yes', 'TechSupport': 'Yes',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'One year', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Bank transfer (automatic)', 'MonthlyCharges': 42.30, 'TotalCharges': 1840.75,
            'churn_pred': 0, 'churn_prob': 0.12, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Invite to VIP Rewards program']
        },
        # 5. High Risk
        {
            'customer_id': '9237-HQJCB', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 2, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 70.70, 'TotalCharges': 151.65,
            'churn_pred': 1, 'churn_prob': 0.85, 'risk_level': 'High Risk',
            'recommendations': ['Immediate Action: Contact customer within 24 hours', 'Offer 15% contract upgrade discount', 'Provide 3 months free Tech Support']
        },
        # 6. High Risk
        {
            'customer_id': '9305-CDSKC', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 8, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'Yes', 'TechSupport': 'No',
            'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 99.65, 'TotalCharges': 820.50,
            'churn_pred': 1, 'churn_prob': 0.82, 'risk_level': 'High Risk',
            'recommendations': ['Immediate Action: Contact customer within 24 hours', 'Perform custom account review for high monthly charges']
        },
        # 7. Medium Risk
        {
            'customer_id': '1452-KNGWZ', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 22, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No', 'OnlineBackup': 'Yes', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'Yes', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Credit card (automatic)', 'MonthlyCharges': 89.10, 'TotalCharges': 1949.40,
            'churn_pred': 1, 'churn_prob': 0.55, 'risk_level': 'Medium Risk',
            'recommendations': ['Proactive Engagement: Send personalized check-in survey', 'Recommend High-Speed Internet Security bundle']
        },
        # 8. Low Risk
        {
            'customer_id': '6713-OKOMC', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 10, 'PhoneService': 'No', 'MultipleLines': 'No phone service', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'No', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Mailed check', 'MonthlyCharges': 29.75, 'TotalCharges': 301.90,
            'churn_pred': 0, 'churn_prob': 0.28, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Maintain regular service touchpoints']
        },
        # 9. High Risk
        {
            'customer_id': '7892-POOKP', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'No',
            'tenure': 28, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'Yes', 'TechSupport': 'Yes',
            'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 104.80, 'TotalCharges': 3046.05,
            'churn_pred': 1, 'churn_prob': 0.74, 'risk_level': 'High Risk',
            'recommendations': ['Immediate Action: Contact customer within 24 hours', 'Offer discount for upgrading contract']
        },
        # 10. Low Risk
        {
            'customer_id': '6388-TABGU', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'Yes',
            'tenure': 62, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'Yes', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'One year', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Bank transfer (automatic)', 'MonthlyCharges': 56.15, 'TotalCharges': 3487.95,
            'churn_pred': 0, 'churn_prob': 0.08, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Invite to VIP Rewards program', 'Offer referral bonus rewards']
        },
        # 11. Low Risk
        {
            'customer_id': '9763-GRSKD', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'Yes',
            'tenure': 13, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'No', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Mailed check', 'MonthlyCharges': 49.95, 'TotalCharges': 587.45,
            'churn_pred': 0, 'churn_prob': 0.22, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Send service satisfaction survey']
        },
        # 12. Low Risk
        {
            'customer_id': '7469-LKBCI', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 16, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'No',
            'OnlineSecurity': 'No internet service', 'OnlineBackup': 'No internet service', 'DeviceProtection': 'No internet service', 'TechSupport': 'No internet service',
            'StreamingTV': 'No internet service', 'StreamingMovies': 'No internet service', 'Contract': 'Two year', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Credit card (automatic)', 'MonthlyCharges': 18.95, 'TotalCharges': 326.80,
            'churn_pred': 0, 'churn_prob': 0.04, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Highly loyal customer']
        },
        # 13. High Risk
        {
            'customer_id': '8091-TTWVR', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'No',
            'tenure': 7, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'Yes', 'TechSupport': 'No',
            'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 105.50, 'TotalCharges': 725.90,
            'churn_pred': 1, 'churn_prob': 0.81, 'risk_level': 'High Risk',
            'recommendations': ['Immediate Action: Priority account retention manager assigned', 'Offer complimentary Online Backup & Security package']
        },
        # 14. Medium Risk
        {
            'customer_id': '5129-JLPIS', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 25, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'No', 'DeviceProtection': 'Yes', 'TechSupport': 'Yes',
            'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 105.45, 'TotalCharges': 2573.55,
            'churn_pred': 1, 'churn_prob': 0.52, 'risk_level': 'Medium Risk',
            'recommendations': ['Proactive Engagement: Send annual service review invite', 'Suggest switching from Electronic Check to Auto-Pay']
        },
        # 15. Low Risk
        {
            'customer_id': '3655-SNQYZ', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'Yes',
            'tenure': 69, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'Yes', 'DeviceProtection': 'Yes', 'TechSupport': 'Yes',
            'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'Two year', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Credit card (automatic)', 'MonthlyCharges': 113.25, 'TotalCharges': 7895.15,
            'churn_pred': 0, 'churn_prob': 0.03, 'risk_level': 'Low Risk',
            'recommendations': ['Loyalty Tier: High-value VIP customer account']
        },
        # 16. High Risk
        {
            'customer_id': '8191-XWSZG', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 5, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'DSL',
            'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Mailed check', 'MonthlyCharges': 20.65, 'TotalCharges': 102.50,
            'churn_pred': 1, 'churn_prob': 0.71, 'risk_level': 'High Risk',
            'recommendations': ['Immediate Action: Outbound loyalty call', 'Offer contract upgrade incentive']
        },
        # 17. Low Risk
        {
            'customer_id': '4737-AQRAX', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'Yes',
            'tenure': 72, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'Yes', 'DeviceProtection': 'Yes', 'TechSupport': 'Yes',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'Two year', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Bank transfer (automatic)', 'MonthlyCharges': 64.80, 'TotalCharges': 4660.00,
            'churn_pred': 0, 'churn_prob': 0.05, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Maintain automated service monitoring']
        },
        # 18. Medium Risk
        {
            'customer_id': '4183-MYHJF', 'gender': 'Female', 'SeniorCitizen': 1, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 14, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No', 'OnlineBackup': 'Yes', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'No', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 74.90, 'TotalCharges': 1035.20,
            'churn_pred': 1, 'churn_prob': 0.68, 'risk_level': 'Medium Risk',
            'recommendations': ['Proactive Engagement: Offer Senior Citizen plan review', 'Provide 1-on-1 Tech Support onboarding']
        },
        # 19. Low Risk
        {
            'customer_id': '1024-KRLVL', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'Yes',
            'tenure': 58, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'Yes', 'DeviceProtection': 'Yes', 'TechSupport': 'Yes',
            'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'Two year', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Credit card (automatic)', 'MonthlyCharges': 85.20, 'TotalCharges': 4941.60,
            'churn_pred': 0, 'churn_prob': 0.09, 'risk_level': 'Low Risk',
            'recommendations': ['Loyalty Tier: Long-term subscriber rewards eligible']
        },
        # 20. High Risk
        {
            'customer_id': '6432-TWLVR', 'gender': 'Male', 'SeniorCitizen': 1, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 3, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 95.80, 'TotalCharges': 287.40,
            'churn_pred': 1, 'churn_prob': 0.89, 'risk_level': 'High Risk',
            'recommendations': ['Immediate Action: Emergency churn intervention team alert', 'Provide bill credit & lock-in rate guarantee']
        },
        # 21. Low Risk
        {
            'customer_id': '2019-CFRXL', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 41, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'No',
            'OnlineSecurity': 'No internet service', 'OnlineBackup': 'No internet service', 'DeviceProtection': 'No internet service', 'TechSupport': 'No internet service',
            'StreamingTV': 'No internet service', 'StreamingMovies': 'No internet service', 'Contract': 'One year', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Mailed check', 'MonthlyCharges': 20.05, 'TotalCharges': 822.05,
            'churn_pred': 0, 'churn_prob': 0.15, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Stable subscriber profile']
        },
        # 22. Medium Risk
        {
            'customer_id': '8779-QRDMV', 'gender': 'Male', 'SeniorCitizen': 1, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 1, 'PhoneService': 'No', 'MultipleLines': 'No phone service', 'InternetService': 'DSL',
            'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'Yes', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'Yes', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 39.65, 'TotalCharges': 39.65,
            'churn_pred': 1, 'churn_prob': 0.62, 'risk_level': 'Medium Risk',
            'recommendations': ['Proactive Engagement: Send welcome guide & feature tutorial']
        },
        # 23. Low Risk
        {
            'customer_id': '3801-HWDJA', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'Yes',
            'tenure': 50, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'Yes', 'DeviceProtection': 'Yes', 'TechSupport': 'No',
            'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'One year', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Bank transfer (automatic)', 'MonthlyCharges': 108.75, 'TotalCharges': 5437.50,
            'churn_pred': 0, 'churn_prob': 0.24, 'risk_level': 'Low Risk',
            'recommendations': ['Standard Engagement: Cross-sell hardware protection plans']
        },
        # 24. High Risk
        {
            'customer_id': '1297-ZKLQW', 'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'No', 'Dependents': 'No',
            'tenure': 4, 'PhoneService': 'Yes', 'MultipleLines': 'No', 'InternetService': 'Fiber optic',
            'OnlineSecurity': 'No', 'OnlineBackup': 'No', 'DeviceProtection': 'No', 'TechSupport': 'No',
            'StreamingTV': 'No', 'StreamingMovies': 'Yes', 'Contract': 'Month-to-month', 'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check', 'MonthlyCharges': 79.85, 'TotalCharges': 319.40,
            'churn_pred': 1, 'churn_prob': 0.83, 'risk_level': 'High Risk',
            'recommendations': ['Immediate Action: Outbound customer success call', 'Offer 1-year contract discount']
        },
        # 25. Low Risk
        {
            'customer_id': '9992-UJBXN', 'gender': 'Female', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'Yes',
            'tenure': 67, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'DSL',
            'OnlineSecurity': 'Yes', 'OnlineBackup': 'Yes', 'DeviceProtection': 'Yes', 'TechSupport': 'Yes',
            'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'Two year', 'PaperlessBilling': 'No',
            'PaymentMethod': 'Bank transfer (automatic)', 'MonthlyCharges': 89.40, 'TotalCharges': 5989.80,
            'churn_pred': 0, 'churn_prob': 0.06, 'risk_level': 'Low Risk',
            'recommendations': ['Loyalty Tier: VIP rewards & priority support member']
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
        
    print(f"Database successfully seeded with {len(sample_customers)} customer prediction records.")

if __name__ == '__main__':
    seed_database()
