"""
Backend utility helpers.
"""
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_path():
    return os.path.join(PROJECT_ROOT, "data", "churn.csv")


def get_model_dir():
    return os.path.join(PROJECT_ROOT, "models")
