"""
Analytics API Routes — EDA and statistics endpoints.
"""
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from flask import Blueprint, jsonify
from src.data_preprocessing import load_data, clean_data
from src.eda import (
    get_overview_stats, get_churn_distribution, get_demographics_analysis,
    get_service_analysis, get_contract_analysis, get_tenure_analysis,
    get_charges_analysis, get_correlation_data
)

analytics_bp = Blueprint("analytics", __name__)

# Cache loaded data
_cached_df = None


def _get_df():
    global _cached_df
    if _cached_df is None:
        data_path = os.path.join(PROJECT_ROOT, "data", "churn.csv")
        _cached_df = load_data(data_path)
    return _cached_df


@analytics_bp.route("/overview")
def overview():
    """Get high-level dataset overview statistics."""
    df = _get_df()
    return jsonify(get_overview_stats(df))


@analytics_bp.route("/churn-distribution")
def churn_distribution():
    """Get churn vs retained distribution."""
    df = _get_df()
    return jsonify(get_churn_distribution(df))


@analytics_bp.route("/demographics")
def demographics():
    """Get demographic analysis of churn."""
    df = _get_df()
    return jsonify(get_demographics_analysis(df))


@analytics_bp.route("/services")
def services():
    """Get service-level churn analysis."""
    df = _get_df()
    return jsonify(get_service_analysis(df))


@analytics_bp.route("/contracts")
def contracts():
    """Get contract and billing churn analysis."""
    df = _get_df()
    return jsonify(get_contract_analysis(df))


@analytics_bp.route("/tenure")
def tenure():
    """Get tenure-based churn analysis."""
    df = _get_df()
    return jsonify(get_tenure_analysis(df))


@analytics_bp.route("/charges")
def charges():
    """Get charges analysis by churn status."""
    df = _get_df()
    return jsonify(get_charges_analysis(df))


@analytics_bp.route("/correlation")
def correlation():
    """Get feature correlation matrix."""
    df = _get_df()
    return jsonify(get_correlation_data(df))
