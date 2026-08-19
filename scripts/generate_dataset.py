import os
import pandas as pd
import numpy as np

def generate_telco_dataset():
    os.makedirs('dataset', exist_ok=True)
    np.random.seed(42)
    n = 7043

    # Generate Customer IDs
    id_chars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    ids = []
    for i in range(n):
        p1 = ''.join(np.random.choice(list('0123456789'), 4))
        p2 = ''.join(np.random.choice(id_chars, 5))
        ids.append(f'{p1}-{p2}')

    gender = np.random.choice(['Female', 'Male'], n)
    senior_citizen = np.random.choice([0, 1], n, p=[0.838, 0.162])
    partner = np.random.choice(['Yes', 'No'], n, p=[0.483, 0.517])
    dependents = np.random.choice(['No', 'Yes'], n, p=[0.700, 0.300])

    tenure = np.random.choice(np.arange(0, 73), n)
    phone_service = np.random.choice(['Yes', 'No'], n, p=[0.903, 0.097])
    
    multiple_lines = []
    for ps in phone_service:
        if ps == 'No':
            multiple_lines.append('No phone service')
        else:
            multiple_lines.append(np.random.choice(['No', 'Yes'], p=[0.53, 0.47]))

    internet_service = np.random.choice(['DSL', 'Fiber optic', 'No'], n, p=[0.34, 0.44, 0.22])

    def get_service_opt(is_opt):
        if is_opt == 'No':
            return 'No internet service'
        return np.random.choice(['No', 'Yes'], p=[0.65, 0.35])

    online_security = [get_service_opt(is_opt) for is_opt in internet_service]
    online_backup = [get_service_opt(is_opt) for is_opt in internet_service]
    device_protection = [get_service_opt(is_opt) for is_opt in internet_service]
    tech_support = [get_service_opt(is_opt) for is_opt in internet_service]
    streaming_tv = [get_service_opt(is_opt) for is_opt in internet_service]
    streaming_movies = [get_service_opt(is_opt) for is_opt in internet_service]

    contract = np.random.choice(['Month-to-month', 'One year', 'Two year'], n, p=[0.55, 0.21, 0.24])
    paperless_billing = np.random.choice(['Yes', 'No'], n, p=[0.59, 0.41])
    payment_method = np.random.choice([
        'Electronic check', 
        'Mailed check', 
        'Bank transfer (automatic)', 
        'Credit card (automatic)'
    ], n, p=[0.34, 0.23, 0.21, 0.22])

    monthly_charges = []
    for i in range(n):
        base = 18.0
        if phone_service[i] == 'Yes': base += 5.0
        if multiple_lines[i] == 'Yes': base += 10.0
        if internet_service[i] == 'DSL': base += 25.0
        elif internet_service[i] == 'Fiber optic': base += 50.0
        
        if online_security[i] == 'Yes': base += 5.0
        if online_backup[i] == 'Yes': base += 5.0
        if device_protection[i] == 'Yes': base += 5.0
        if tech_support[i] == 'Yes': base += 5.0
        if streaming_tv[i] == 'Yes': base += 10.0
        if streaming_movies[i] == 'Yes': base += 10.0
        
        noise = np.random.normal(0, 2)
        monthly_charges.append(round(max(18.25, base + noise), 2))

    total_charges = []
    for i in range(n):
        if tenure[i] == 0:
            total_charges.append(' ')  # Blank values as in original Telco CSV
        else:
            tc = monthly_charges[i] * tenure[i] + np.random.normal(0, 10)
            total_charges.append(f'{round(max(18.25, tc), 2):.2f}')

    # Calculation for realistic ground truth churn probability
    z = -1.2
    z += np.where(np.array(contract) == 'Month-to-month', 1.4, -0.6)
    z += np.where(np.array(internet_service) == 'Fiber optic', 0.9, -0.3)
    z += np.where(np.array(payment_method) == 'Electronic check', 0.5, -0.2)
    z += np.where(np.array(tech_support) == 'No', 0.5, -0.4)
    z += np.where(np.array(online_security) == 'No', 0.4, -0.3)
    z += (11.0 / (np.array(tenure) + 1.0)) * 0.4
    z += (np.array(monthly_charges) - 64.0) / 40.0 * 0.5
    z += np.where(np.array(senior_citizen) == 1, 0.3, 0.0)

    prob = 1 / (1 + np.exp(-z))
    churn = np.where(prob > np.percentile(prob, 73.5), 'Yes', 'No')

    df = pd.DataFrame({
        'customerID': ids,
        'gender': gender,
        'SeniorCitizen': senior_citizen,
        'Partner': partner,
        'Dependents': dependents,
        'tenure': tenure,
        'PhoneService': phone_service,
        'MultipleLines': multiple_lines,
        'InternetService': internet_service,
        'OnlineSecurity': online_security,
        'OnlineBackup': online_backup,
        'DeviceProtection': device_protection,
        'TechSupport': tech_support,
        'StreamingTV': streaming_tv,
        'StreamingMovies': streaming_movies,
        'Contract': contract,
        'PaperlessBilling': paperless_billing,
        'PaymentMethod': payment_method,
        'MonthlyCharges': monthly_charges,
        'TotalCharges': total_charges,
        'Churn': churn
    })

    file_path = 'dataset/WA_Fn-UseC_-Telco-Customer-Churn.csv'
    df.to_csv(file_path, index=False)
    print(f"Dataset generated and saved to {file_path}")
    print(f"Shape: {df.shape}")
    print("Churn breakdown:")
    print(df['Churn'].value_counts())

if __name__ == '__main__':
    generate_telco_dataset()
