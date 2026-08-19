import sqlite3
import os
import json
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join('database', 'churn.db')


def get_db_connection():
    """Create and return a database connection with Row factory."""
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables for users and predictions."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Predictions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            customer_id TEXT,
            gender TEXT,
            senior_citizen INTEGER,
            partner TEXT,
            dependents TEXT,
            tenure INTEGER,
            phone_service TEXT,
            multiple_lines TEXT,
            internet_service TEXT,
            online_security TEXT,
            online_backup TEXT,
            device_protection TEXT,
            tech_support TEXT,
            streaming_tv TEXT,
            streaming_movies TEXT,
            contract TEXT,
            paperless_billing TEXT,
            payment_method TEXT,
            monthly_charges REAL,
            total_charges REAL,
            churn_prediction INTEGER,
            churn_probability REAL,
            risk_level TEXT,
            retention_recommendations TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()


def register_user(username, password):
    """Register a new user with hashed password."""
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    try:
        cursor.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists"


def get_user_by_username(username):
    """Retrieve user record by username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user


def save_prediction(user_id, data, churn_pred, churn_prob, risk_level, recommendations):
    """Save customer input data and model prediction results into database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    recs_json = json.dumps(recommendations)
    
    cursor.execute('''
        INSERT INTO predictions (
            user_id, customer_id, gender, senior_citizen, partner, dependents,
            tenure, phone_service, multiple_lines, internet_service, online_security,
            online_backup, device_protection, tech_support, streaming_tv, streaming_movies,
            contract, paperless_billing, payment_method, monthly_charges, total_charges,
            churn_prediction, churn_probability, risk_level, retention_recommendations
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        data.get('customer_id', 'CUST-' + str(np_random_id())),
        data.get('gender', 'Male'),
        int(data.get('SeniorCitizen', 0)),
        data.get('Partner', 'No'),
        data.get('Dependents', 'No'),
        int(data.get('tenure', 0)),
        data.get('PhoneService', 'Yes'),
        data.get('MultipleLines', 'No'),
        data.get('InternetService', 'DSL'),
        data.get('OnlineSecurity', 'No'),
        data.get('OnlineBackup', 'No'),
        data.get('DeviceProtection', 'No'),
        data.get('TechSupport', 'No'),
        data.get('StreamingTV', 'No'),
        data.get('StreamingMovies', 'No'),
        data.get('Contract', 'Month-to-month'),
        data.get('PaperlessBilling', 'Yes'),
        data.get('PaymentMethod', 'Electronic check'),
        float(data.get('MonthlyCharges', 0.0)),
        float(data.get('TotalCharges', 0.0)),
        int(churn_pred),
        float(churn_prob),
        risk_level,
        recs_json
    ))
    
    conn.commit()
    pred_id = cursor.lastrowid
    conn.close()
    return pred_id


def np_random_id():
    import random
    return random.randint(10000, 99999)


def get_all_predictions(search_query=None, risk_filter=None):
    """Retrieve predictions with optional search and risk level filtering."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM predictions WHERE 1=1'
    params = []
    
    if search_query:
        query += ' AND (customer_id LIKE ? OR payment_method LIKE ? OR contract LIKE ?)'
        wildcard = f'%{search_query}%'
        params.extend([wildcard, wildcard, wildcard])
        
    if risk_filter and risk_filter.lower() != 'all':
        query += ' AND risk_level = ?'
        params.append(risk_filter)
        
    query += ' ORDER BY created_at DESC'
    
    rows = cursor.execute(query, params).fetchall()
    conn.close()
    
    # Parse json recommendations
    results = []
    for r in rows:
        dict_row = dict(r)
        try:
            dict_row['recommendations'] = json.loads(dict_row['retention_recommendations'])
        except Exception:
            dict_row['recommendations'] = [dict_row['retention_recommendations']]
        results.append(dict_row)
        
    return results


def get_prediction_by_id(pred_id):
    """Retrieve a single prediction by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute('SELECT * FROM predictions WHERE id = ?', (pred_id,)).fetchone()
    conn.close()
    
    if row:
        dict_row = dict(row)
        try:
            dict_row['recommendations'] = json.loads(dict_row['retention_recommendations'])
        except Exception:
            dict_row['recommendations'] = [dict_row['retention_recommendations']]
        return dict_row
    return None


def delete_prediction(pred_id):
    """Delete a prediction record by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM predictions WHERE id = ?', (pred_id,))
    conn.commit()
    conn.close()
    return True


def get_dashboard_stats():
    """Calculate key business intelligence dashboard metrics."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    total = cursor.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
    
    if total == 0:
        conn.close()
        return {
            'total_predictions': 0,
            'churned_count': 0,
            'retained_count': 0,
            'churn_rate': 0.0,
            'high_risk_count': 0,
            'medium_risk_count': 0,
            'low_risk_count': 0,
            'avg_monthly_charges': 0.0,
            'avg_tenure': 0.0,
            'contract_dist': {},
            'internet_dist': {}
        }
        
    churned = cursor.execute('SELECT COUNT(*) FROM predictions WHERE churn_prediction = 1').fetchone()[0]
    retained = total - churned
    churn_rate = round((churned / total) * 100, 2)
    
    high_risk = cursor.execute("SELECT COUNT(*) FROM predictions WHERE risk_level = 'High Risk'").fetchone()[0]
    med_risk = cursor.execute("SELECT COUNT(*) FROM predictions WHERE risk_level = 'Medium Risk'").fetchone()[0]
    low_risk = cursor.execute("SELECT COUNT(*) FROM predictions WHERE risk_level = 'Low Risk'").fetchone()[0]
    
    avg_monthly = cursor.execute('SELECT AVG(monthly_charges) FROM predictions').fetchone()[0] or 0.0
    avg_tenure = cursor.execute('SELECT AVG(tenure) FROM predictions').fetchone()[0] or 0.0
    
    # Contract Distribution
    contract_rows = cursor.execute('SELECT contract, COUNT(*) as cnt FROM predictions GROUP BY contract').fetchall()
    contract_dist = {r['contract']: r['cnt'] for r in contract_rows}
    
    # Internet Service Distribution
    internet_rows = cursor.execute('SELECT internet_service, COUNT(*) as cnt FROM predictions GROUP BY internet_service').fetchall()
    internet_dist = {r['internet_service']: r['cnt'] for r in internet_rows}
    
    conn.close()
    
    return {
        'total_predictions': total,
        'churned_count': churned,
        'retained_count': retained,
        'churn_rate': churn_rate,
        'high_risk_count': high_risk,
        'medium_risk_count': med_risk,
        'low_risk_count': low_risk,
        'avg_monthly_charges': round(avg_monthly, 2),
        'avg_tenure': round(avg_tenure, 1),
        'contract_dist': contract_dist,
        'internet_dist': internet_dist
    }
