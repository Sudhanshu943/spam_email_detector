"""
Configuration settings for Spam Email Detector application
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

EMAILS_PER_PAGE = 10

TEXT_VALIDATION = {
    "min_length": 1,
    "max_length": 100000,
}

EMAIL_VALIDATION = {
    "max_size": 1000000,
}

MODEL_CONFIG = {
    "tfidf_max_features": 2000,
    "test_size": 0.2,
    "random_state": 2,
}

PATHS = {
    "config_dir": os.path.join(BASE_DIR, "config"),
    "credentials_file": os.path.join(BASE_DIR, "config", "credentials.json"),
    "token_file": os.path.join(BASE_DIR, "config", "token.json"),
    "models_dir": os.path.join(BASE_DIR, "models"),
    "vectorizer_file": os.path.join(BASE_DIR, "models", "vectorizer.pkl"),
    "model_file": os.path.join(BASE_DIR, "models", "model.pkl"),
    "dataset_file": os.path.join(BASE_DIR, "dataset", "spam.csv"),
}

LOGGING_CONFIG = {
    "log_dir": os.path.join(BASE_DIR, "logs"),
    "log_file": os.path.join(BASE_DIR, "logs", "app.log"),
    "level": "INFO",
}

UI_CONFIG = {
    "page_title": "Spam Email Detector",
    "page_icon": "📧",
    "layout": "wide",
    "preview_length": 500,
    "max_links_display": 3,
}

PREDICTION_CONFIDENCE = {
    "high_threshold": 0.8,
    "low_threshold": 0.5,
}

ERROR_MESSAGES = {
    "model_not_found": "Model files not found in 'models/' folder",
    "credentials_not_found": "config/credentials.json file not found. Please add your Google API credentials.",
    "invalid_input": "Input validation failed",
    "email_fetch_error": "Error fetching emails",
    "prediction_error": "Model prediction error",
    "authentication_error": "Failed to authenticate with Google API",
}

SUCCESS_MESSAGES = {
    "analysis_complete": "Analysis completed successfully",
    "email_validated": "Email validated successfully",
}
