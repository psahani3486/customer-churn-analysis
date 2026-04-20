"""
Data Preprocessing Module for Customer Churn Analysis
Handles data loading, cleaning, encoding, and feature engineering.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "churn.csv")


def load_data(path=None):
    """Load the churn dataset from CSV."""
    if path is None:
        path = DATA_PATH
    df = pd.read_csv(path)
    return df


def clean_data(df):
    """
    Clean the dataset:
    - Convert TotalCharges to numeric (handle whitespace)
    - Drop customerID (not a feature)
    - Handle missing values
    """
    df = df.copy()

    # TotalCharges has some whitespace values — convert to numeric
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # Fill missing TotalCharges with median
    df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

    # Drop customerID — not useful for modeling
    if "customerID" in df.columns:
        df.drop("customerID", axis=1, inplace=True)

    return df


def encode_features(df):
    """
    Encode categorical features:
    - Binary columns: LabelEncoder
    - Multi-class columns: One-hot encoding
    """
    df = df.copy()

    # Binary columns
    binary_cols = ["gender", "Partner", "Dependents", "PhoneService",
                   "PaperlessBilling", "Churn"]
    le = LabelEncoder()
    for col in binary_cols:
        if col in df.columns:
            df[col] = le.fit_transform(df[col])

    # Multi-class columns — one-hot encode
    multi_cols = ["MultipleLines", "InternetService", "OnlineSecurity",
                  "OnlineBackup", "DeviceProtection", "TechSupport",
                  "StreamingTV", "StreamingMovies", "Contract",
                  "PaymentMethod"]
    df = pd.get_dummies(df, columns=multi_cols, drop_first=True)

    return df


def get_feature_target(df, target_col="Churn"):
    """Split dataframe into features (X) and target (y)."""
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    return X, y


def scale_features(X_train, X_test):
    """Scale numerical features using StandardScaler."""
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns,
        index=X_test.index
    )
    return X_train_scaled, X_test_scaled, scaler


def preprocess_pipeline(path=None, test_size=0.2, random_state=42):
    """
    Full preprocessing pipeline:
    1. Load data
    2. Clean data
    3. Encode features
    4. Split train/test
    5. Scale features

    Returns:
        X_train, X_test, y_train, y_test, scaler, raw_df
    """
    raw_df = load_data(path)
    df = clean_data(raw_df)
    df = encode_features(df)

    X, y = get_feature_target(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, raw_df


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, scaler, raw_df = preprocess_pipeline()
    print(f"[OK] Preprocessing complete")
    print(f"   Raw shape: {raw_df.shape}")
    print(f"   Training set: {X_train.shape}")
    print(f"   Test set: {X_test.shape}")
    print(f"   Features: {X_train.shape[1]}")
    print(f"   Churn rate: {y_train.mean():.1%}")
