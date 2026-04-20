"""
Predictions API Routes — Model training, evaluation, and prediction endpoints.
"""
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from flask import Blueprint, jsonify, request
from src.data_preprocessing import preprocess_pipeline
from src.model import run_full_pipeline, predict_single

predictions_bp = Blueprint("predictions", __name__)

# Cache model results
_model_results = None
_scaler = None
_feature_names = None


def _ensure_models():
    """Train models if not already done."""
    global _model_results, _scaler, _feature_names
    if _model_results is None:
        data_path = os.path.join(PROJECT_ROOT, "data", "churn.csv")
        X_train, X_test, y_train, y_test, scaler, raw_df = preprocess_pipeline(data_path)
        _scaler = scaler
        _feature_names = X_train.columns.tolist()
        _model_results = run_full_pipeline(X_train, X_test, y_train, y_test, scaler)
    return _model_results


@predictions_bp.route("/model-performance")
def model_performance():
    """Get performance metrics for all trained models."""
    results = _ensure_models()
    return jsonify({
        "models": results["model_performance"],
        "best_model": results["best_model"]
    })


@predictions_bp.route("/feature-importance")
def feature_importance():
    """Get top feature importances from best model."""
    results = _ensure_models()
    return jsonify(results["feature_importance"])


@predictions_bp.route("/risk-segments")
def risk_segments():
    """Get customer risk segmentation."""
    results = _ensure_models()
    return jsonify(results["risk_segments"])


@predictions_bp.route("/predict", methods=["POST"])
def predict():
    """
    Predict churn for a single customer.
    Expects JSON body with customer features.
    """
    results = _ensure_models()
    customer_data = request.get_json()

    if not customer_data:
        return jsonify({"error": "No customer data provided"}), 400

    best_model = results["fitted_models"][results["best_model"]]
    prediction = predict_single(best_model, _scaler, _feature_names, customer_data)

    return jsonify(prediction)
