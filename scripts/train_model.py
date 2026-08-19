import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix
)

# Import column definitions
import sys
sys.path.append('.')
from utils.preprocessing import NUMERICAL_FEATURES, CATEGORICAL_FEATURES, clean_dataframe


def train_and_evaluate_models():
    os.makedirs('model', exist_ok=True)
    dataset_path = 'dataset/WA_Fn-UseC_-Telco-Customer-Churn.csv'
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")
    
    df = pd.read_csv(dataset_path)
    print(f"Loaded raw dataset with shape: {df.shape}")
    
    # 1. Clean dataset
    df_clean = clean_dataframe(df)
    print(f"Dataset after cleaning: {df_clean.shape}")
    
    # 2. Encode target variable Churn (Yes -> 1, No -> 0)
    df_clean['Churn'] = df_clean['Churn'].map({'Yes': 1, 'No': 0})
    
    X = df_clean[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    y = df_clean['Churn']
    
    # 3. Train/Test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Training set: {X_train.shape[0]} rows, Test set: {X_test.shape[0]} rows")
    
    # 4. Preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), NUMERICAL_FEATURES),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL_FEATURES)
        ]
    )
    
    # Fit preprocessor to get feature names for feature importance analysis
    preprocessor.fit(X_train)
    cat_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(CATEGORICAL_FEATURES)
    all_transformed_feature_names = list(NUMERICAL_FEATURES) + list(cat_feature_names)
    
    # 5. Define ML Models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
    }
    
    model_metrics = {}
    fitted_pipelines = {}
    
    print("\n--- Training and Evaluating Models ---")
    for name, clf in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])
        
        pipeline.fit(X_train, y_train)
        fitted_pipelines[name] = pipeline
        
        y_pred = pipeline.predict(X_test)
        y_proba = pipeline.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_proba)
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        model_metrics[name] = {
            'accuracy': float(acc),
            'precision': float(prec),
            'recall': float(rec),
            'f1_score': float(f1),
            'roc_auc': float(roc_auc),
            'confusion_matrix': cm
        }
        
        print(f"{name:20s} | Accuracy: {acc*100:.2f}% | Precision: {prec*100:.2f}% | Recall: {rec*100:.2f}% | F1: {f1*100:.2f}% | ROC-AUC: {roc_auc:.4f}")
    
    # Select best model based on ROC-AUC
    best_model_name = max(model_metrics, key=lambda k: model_metrics[k]['roc_auc'])
    print(f"\nBest Model Selected based on ROC-AUC: {best_model_name} (ROC-AUC = {model_metrics[best_model_name]['roc_auc']:.4f})")
    
    best_pipeline = fitted_pipelines[best_model_name]
    
    # Save best model pipeline
    model_save_path = 'model/churn_model.pkl'
    joblib.dump(best_pipeline, model_save_path)
    print(f"Saved trained model pipeline to {model_save_path}")
    
    # Extract Feature Importances from best model if available
    classifier = best_pipeline.named_steps['classifier']
    feature_importances = []
    
    if hasattr(classifier, 'feature_importances_'):
        importances = classifier.feature_importances_
        feature_imp_pairs = sorted(zip(all_transformed_feature_names, importances), key=lambda x: x[1], reverse=True)
        feature_importances = [{'feature': f, 'importance': float(i)} for f, i in feature_imp_pairs[:10]]
    
    metrics_summary = {
        'best_model': best_model_name,
        'selected_by': 'ROC-AUC',
        'metrics': model_metrics,
        'feature_importances': feature_importances
    }
    
    metrics_save_path = 'model/model_metrics.json'
    with open(metrics_save_path, 'w') as f:
        json.dump(metrics_summary, f, indent=4)
    print(f"Saved model metrics and feature importances to {metrics_save_path}")
    
    return metrics_summary


if __name__ == '__main__':
    train_and_evaluate_models()
