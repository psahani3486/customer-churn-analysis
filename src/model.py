"""
Machine Learning Model Module for Customer Churn Prediction.
Trains multiple classifiers, evaluates performance, and provides predictions.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, classification_report
)
import joblib
import os

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")


def get_models():
    """Return dictionary of models to train (optimized for low-memory environments)."""
    return {
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=8, random_state=42
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=80, max_depth=4, learning_rate=0.1, random_state=42
        ),
        "Logistic Regression": LogisticRegression(
            max_iter=1000, random_state=42, C=0.5
        )
    }


def train_models(X_train, y_train):
    """Train all models and return fitted models."""
    models = get_models()
    fitted = {}
    for name, model in models.items():
        print(f"   Training {name}...")
        model.fit(X_train, y_train)
        fitted[name] = model
    return fitted


def evaluate_model(model, X_test, y_test):
    """Evaluate a single model and return metrics."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
        "precision": round(precision_score(y_test, y_pred, zero_division=0) * 100, 2),
        "recall": round(recall_score(y_test, y_pred, zero_division=0) * 100, 2),
        "f1_score": round(f1_score(y_test, y_pred, zero_division=0) * 100, 2),
    }

    if y_proba is not None:
        metrics["roc_auc"] = round(roc_auc_score(y_test, y_proba) * 100, 2)

    cm = confusion_matrix(y_test, y_pred)
    metrics["confusion_matrix"] = {
        "true_negative": int(cm[0][0]),
        "false_positive": int(cm[0][1]),
        "false_negative": int(cm[1][0]),
        "true_positive": int(cm[1][1])
    }

    return metrics


def evaluate_all_models(fitted_models, X_test, y_test):
    """Evaluate all trained models and return comparison."""
    results = {}
    for name, model in fitted_models.items():
        results[name] = evaluate_model(model, X_test, y_test)
    return results


def get_feature_importance(model, feature_names, top_n=15):
    """Extract feature importance from a model."""
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_[0])
    else:
        return {"features": [], "importances": []}

    # Sort by importance
    indices = np.argsort(importances)[::-1][:top_n]
    top_features = [feature_names[i] for i in indices]
    top_importances = [round(float(importances[i]), 4) for i in indices]

    return {
        "features": top_features,
        "importances": top_importances
    }


def get_risk_segments(model, X_test, y_test):
    """Segment customers into risk categories based on churn probability."""
    if not hasattr(model, "predict_proba"):
        return {"high": 0, "medium": 0, "low": 0}

    probas = model.predict_proba(X_test)[:, 1]

    high_risk = int((probas >= 0.7).sum())
    medium_risk = int(((probas >= 0.3) & (probas < 0.7)).sum())
    low_risk = int((probas < 0.3).sum())

    return {
        "high": high_risk,
        "medium": medium_risk,
        "low": low_risk,
        "high_pct": round(high_risk / len(probas) * 100, 1),
        "medium_pct": round(medium_risk / len(probas) * 100, 1),
        "low_pct": round(low_risk / len(probas) * 100, 1)
    }


def save_model(model, name, scaler=None):
    """Save trained model to disk."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, f"{name.lower().replace(' ', '_')}.joblib")
    joblib.dump(model, model_path)
    if scaler:
        scaler_path = os.path.join(MODEL_DIR, "scaler.joblib")
        joblib.dump(scaler, scaler_path)
    return model_path


def load_model(name):
    """Load a trained model from disk."""
    model_path = os.path.join(MODEL_DIR, f"{name.lower().replace(' ', '_')}.joblib")
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None


def predict_single(model, scaler, feature_names, customer_data):
    """
    Predict churn for a single customer.
    customer_data: dict of feature values
    """
    df = pd.DataFrame([customer_data])

    # Ensure all expected columns exist
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_names]
    df_scaled = pd.DataFrame(scaler.transform(df), columns=feature_names)

    prediction = int(model.predict(df_scaled)[0])
    probability = round(float(model.predict_proba(df_scaled)[0][1]) * 100, 1)

    return {
        "prediction": "Churn" if prediction == 1 else "No Churn",
        "churn_probability": probability,
        "risk_level": "High" if probability >= 70 else ("Medium" if probability >= 30 else "Low")
    }


def run_full_pipeline(X_train, X_test, y_train, y_test, scaler=None):
    """
    Run the complete model training and evaluation pipeline.
    Returns all results needed by the API.
    """
    print(">> Training models...")
    fitted_models = train_models(X_train, y_train)

    print(">> Evaluating models...")
    evaluations = evaluate_all_models(fitted_models, X_test, y_test)

    # Use best model (by F1 score) for feature importance and risk segments
    best_name = max(evaluations, key=lambda k: evaluations[k]["f1_score"])
    best_model = fitted_models[best_name]

    feature_importance = get_feature_importance(
        best_model, X_train.columns.tolist()
    )
    risk_segments = get_risk_segments(best_model, X_test, y_test)

    # Save best model
    print(f">> Saving best model ({best_name})...")
    save_model(best_model, best_name, scaler)

    return {
        "model_performance": evaluations,
        "best_model": best_name,
        "feature_importance": feature_importance,
        "risk_segments": risk_segments,
        "fitted_models": fitted_models
    }


if __name__ == "__main__":
    from data_preprocessing import preprocess_pipeline

    X_train, X_test, y_train, y_test, scaler, raw_df = preprocess_pipeline()
    results = run_full_pipeline(X_train, X_test, y_train, y_test, scaler)

    print(f"\n[OK] Pipeline complete!")
    print(f"   Best model: {results['best_model']}")
    for name, metrics in results["model_performance"].items():
        print(f"   {name}: Accuracy={metrics['accuracy']}%, F1={metrics['f1_score']}%")
