import os
import io
import json
import csv
import joblib
import pandas as pd
import numpy as np
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, jsonify, Response
)
from werkzeug.security import check_password_hash

from utils.database import (
    init_db, register_user, get_user_by_username,
    save_prediction, get_all_predictions, get_prediction_by_id,
    delete_prediction, get_dashboard_stats
)
from utils.preprocessing import (
    clean_dataframe, get_risk_level, get_retention_recommendations,
    NUMERICAL_FEATURES, CATEGORICAL_FEATURES, ALL_INPUT_FEATURES
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'customer_churn_prediction_secret_key_2026')

# Initialize DB on startup
init_db()

# Load trained Machine Learning model pipeline
MODEL_PATH = os.path.join('model', 'churn_model.pkl')
METRICS_PATH = os.path.join('model', 'model_metrics.json')

model_pipeline = None
if os.path.exists(MODEL_PATH):
    try:
        model_pipeline = joblib.load(MODEL_PATH)
        print("Trained model pipeline loaded successfully.")
    except Exception as e:
        print(f"Error loading model pipeline: {e}")
else:
    print("Warning: Trained model pipeline not found at model/churn_model.pkl.")


# Helper: Check if logged in
def is_logged_in():
    return 'user_id' in session


@app.context_processor
def inject_user():
    return {
        'logged_in': is_logged_in(),
        'username': session.get('username', '')
    }


# -------------------------------------------------------------
# AUTHENTICATION ROUTES
# -------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        success, message = register_user(username, password)
        if success:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# -------------------------------------------------------------
# MAIN APP ROUTES
# -------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if model_pipeline is None:
            flash('Trained model is not available. Please train the model first.', 'danger')
            return redirect(url_for('predict'))

        try:
            # Extract 19 input features from form
            customer_data = {
                'customer_id': request.form.get('customer_id', f"CUST-{np.random.randint(10000, 99999)}").strip(),
                'gender': request.form.get('gender', 'Male'),
                'SeniorCitizen': int(request.form.get('SeniorCitizen', 0)),
                'Partner': request.form.get('Partner', 'No'),
                'Dependents': request.form.get('Dependents', 'No'),
                'tenure': float(request.form.get('tenure', 1)),
                'PhoneService': request.form.get('PhoneService', 'Yes'),
                'MultipleLines': request.form.get('MultipleLines', 'No'),
                'InternetService': request.form.get('InternetService', 'DSL'),
                'OnlineSecurity': request.form.get('OnlineSecurity', 'No'),
                'OnlineBackup': request.form.get('OnlineBackup', 'No'),
                'DeviceProtection': request.form.get('DeviceProtection', 'No'),
                'TechSupport': request.form.get('TechSupport', 'No'),
                'StreamingTV': request.form.get('StreamingTV', 'No'),
                'StreamingMovies': request.form.get('StreamingMovies', 'No'),
                'Contract': request.form.get('Contract', 'Month-to-month'),
                'PaperlessBilling': request.form.get('PaperlessBilling', 'Yes'),
                'PaymentMethod': request.form.get('PaymentMethod', 'Electronic check'),
                'MonthlyCharges': float(request.form.get('MonthlyCharges', 50.0)),
                'TotalCharges': float(request.form.get('TotalCharges', 50.0))
            }

            # Prepare dataframe for prediction
            input_df = pd.DataFrame([customer_data])[ALL_INPUT_FEATURES]

            # Execute pipeline prediction
            churn_prediction = int(model_pipeline.predict(input_df)[0])
            churn_probability = float(model_pipeline.predict_proba(input_df)[0][1])

            # Classify Risk Level and Recommendations
            risk_level = get_risk_level(churn_probability)
            recommendations = get_retention_recommendations(risk_level, customer_data)

            # Save prediction record to SQLite Database
            user_id = session.get('user_id')
            pred_id = save_prediction(
                user_id=user_id,
                data=customer_data,
                churn_pred=churn_prediction,
                churn_prob=churn_probability,
                risk_level=risk_level,
                recommendations=recommendations
            )

            flash('Churn prediction completed successfully!', 'success')
            return redirect(url_for('result', prediction_id=pred_id))

        except Exception as e:
            flash(f'Error processing prediction input: {str(e)}', 'danger')
            return redirect(url_for('predict'))

    return render_template('predict.html')


@app.route('/result/<int:prediction_id>')
def result(prediction_id):
    prediction = get_prediction_by_id(prediction_id)
    if not prediction:
        flash('Prediction record not found.', 'danger')
        return redirect(url_for('customers'))

    return render_template('result.html', prediction=prediction)


@app.route('/dashboard')
def dashboard():
    stats = get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)


@app.route('/customers')
def customers():
    search_query = request.args.get('q', '').strip()
    risk_filter = request.args.get('risk', 'all').strip()

    predictions_list = get_all_predictions(search_query=search_query, risk_filter=risk_filter)
    return render_template(
        'customers.html',
        predictions=predictions_list,
        search_query=search_query,
        risk_filter=risk_filter
    )


@app.route('/delete_prediction/<int:prediction_id>', methods=['POST'])
def delete_prediction_route(prediction_id):
    delete_prediction(prediction_id)
    flash(f'Prediction record #{prediction_id} deleted successfully.', 'success')
    return redirect(url_for('customers'))


@app.route('/analytics')
def analytics():
    metrics_data = {}
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, 'r') as f:
                metrics_data = json.load(f)
        except Exception as e:
            print(f"Error reading metrics JSON: {e}")

    return render_template('analytics.html', metrics_data=metrics_data)


@app.route('/export_csv')
def export_csv():
    predictions_list = get_all_predictions()

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        'ID', 'Customer ID', 'Gender', 'Senior Citizen', 'Partner', 'Dependents',
        'Tenure (Months)', 'Phone Service', 'Multiple Lines', 'Internet Service',
        'Online Security', 'Online Backup', 'Device Protection', 'Tech Support',
        'Streaming TV', 'Streaming Movies', 'Contract', 'Paperless Billing',
        'Payment Method', 'Monthly Charges ($)', 'Total Charges ($)',
        'Churn Prediction', 'Churn Probability (%)', 'Risk Level', 'Created At'
    ])

    for p in predictions_list:
        writer.writerow([
            p['id'], p['customer_id'], p['gender'], p['senior_citizen'], p['partner'], p['dependents'],
            p['tenure'], p['phone_service'], p['multiple_lines'], p['internet_service'],
            p['online_security'], p['online_backup'], p['device_protection'], p['tech_support'],
            p['streaming_tv'], p['streaming_movies'], p['contract'], p['paperless_billing'],
            p['payment_method'], p['monthly_charges'], p['total_charges'],
            'Churn' if p['churn_prediction'] == 1 else 'No Churn',
            f"{p['churn_probability'] * 100:.2f}%", p['risk_level'], p['created_at']
        ])

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=customer_churn_predictions.csv'
    return response


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
