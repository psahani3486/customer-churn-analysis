"""
Exploratory Data Analysis Module for Customer Churn Analysis.
Generates statistics and JSON-serializable data for the frontend dashboard.
"""
import pandas as pd
import numpy as np
from .data_preprocessing import load_data, clean_data


def get_overview_stats(df):
    """Get high-level overview statistics."""
    churn_counts = df["Churn"].value_counts()
    churn_rate = (churn_counts.get("Yes", 0) / len(df)) * 100

    return {
        "total_customers": int(len(df)),
        "churned_customers": int(churn_counts.get("Yes", 0)),
        "retained_customers": int(churn_counts.get("No", 0)),
        "churn_rate": round(churn_rate, 1),
        "avg_tenure": round(df["tenure"].mean(), 1),
        "avg_monthly_charges": round(df["MonthlyCharges"].mean(), 2),
        "avg_total_charges": round(pd.to_numeric(df["TotalCharges"], errors="coerce").mean(), 2),
        "senior_citizen_pct": round((df["SeniorCitizen"].mean()) * 100, 1),
    }


def get_churn_distribution(df):
    """Get churn distribution counts."""
    counts = df["Churn"].value_counts().to_dict()
    return {
        "labels": list(counts.keys()),
        "values": list(counts.values()),
        "percentages": [round(v / len(df) * 100, 1) for v in counts.values()]
    }


def get_churn_by_feature(df, feature):
    """Get churn breakdown for a given categorical feature."""
    cross = pd.crosstab(df[feature], df["Churn"])
    result = {
        "labels": cross.index.tolist(),
        "churned": cross.get("Yes", pd.Series([0]*len(cross))).tolist(),
        "retained": cross.get("No", pd.Series([0]*len(cross))).tolist()
    }
    return result


def get_demographics_analysis(df):
    """Analyze churn across demographic features."""
    demographics = {}
    for col in ["gender", "SeniorCitizen", "Partner", "Dependents"]:
        if col == "SeniorCitizen":
            temp = df.copy()
            temp["SeniorCitizen"] = temp["SeniorCitizen"].map({0: "No", 1: "Yes"})
            demographics[col] = get_churn_by_feature(temp, col)
        else:
            demographics[col] = get_churn_by_feature(df, col)
    return demographics


def get_service_analysis(df):
    """Analyze churn across service features."""
    services = {}
    service_cols = [
        "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies"
    ]
    for col in service_cols:
        if col in df.columns:
            services[col] = get_churn_by_feature(df, col)
    return services


def get_contract_analysis(df):
    """Analyze churn by contract type, billing, and payment method."""
    return {
        "contract": get_churn_by_feature(df, "Contract"),
        "paperless_billing": get_churn_by_feature(df, "PaperlessBilling"),
        "payment_method": get_churn_by_feature(df, "PaymentMethod")
    }


def get_tenure_analysis(df):
    """Analyze churn rate across tenure bins."""
    df = df.copy()
    df["tenure_group"] = pd.cut(
        df["tenure"],
        bins=[0, 6, 12, 24, 36, 48, 60, 72],
        labels=["0-6", "7-12", "13-24", "25-36", "37-48", "49-60", "61-72"]
    )
    tenure_churn = df.groupby("tenure_group", observed=False)["Churn"].apply(
        lambda x: round((x == "Yes").mean() * 100, 1)
    )
    return {
        "labels": tenure_churn.index.tolist(),
        "churn_rates": tenure_churn.values.tolist(),
        "counts": df["tenure_group"].value_counts().sort_index().tolist()
    }


def get_charges_analysis(df):
    """Analyze monthly and total charges distribution by churn status."""
    churned = df[df["Churn"] == "Yes"]
    retained = df[df["Churn"] == "No"]

    return {
        "monthly_charges": {
            "churned_mean": round(churned["MonthlyCharges"].mean(), 2),
            "retained_mean": round(retained["MonthlyCharges"].mean(), 2),
            "churned_median": round(churned["MonthlyCharges"].median(), 2),
            "retained_median": round(retained["MonthlyCharges"].median(), 2),
        },
        "total_charges": {
            "churned_mean": round(pd.to_numeric(churned["TotalCharges"], errors="coerce").mean(), 2),
            "retained_mean": round(pd.to_numeric(retained["TotalCharges"], errors="coerce").mean(), 2),
        },
        "monthly_bins": _bin_charges(df, "MonthlyCharges")
    }


def _bin_charges(df, col):
    """Create binned charge distribution."""
    df = df.copy()
    bins = pd.cut(df[col], bins=10)
    result = df.groupby(bins, observed=False)["Churn"].apply(
        lambda x: round((x == "Yes").mean() * 100, 1)
    )
    return {
        "labels": [str(b) for b in result.index.tolist()],
        "churn_rates": result.values.tolist()
    }


def get_correlation_data(df):
    """Get correlation matrix for numeric features."""
    df_clean = clean_data(df)
    numeric_df = df_clean.select_dtypes(include=[np.number])
    corr = numeric_df.corr().round(3)
    return {
        "features": corr.columns.tolist(),
        "matrix": corr.values.tolist()
    }


def run_full_eda(path=None):
    """Run the complete EDA pipeline and return all results."""
    df = load_data(path)

    return {
        "overview": get_overview_stats(df),
        "churn_distribution": get_churn_distribution(df),
        "demographics": get_demographics_analysis(df),
        "services": get_service_analysis(df),
        "contracts": get_contract_analysis(df),
        "tenure": get_tenure_analysis(df),
        "charges": get_charges_analysis(df),
        "correlation": get_correlation_data(df)
    }
