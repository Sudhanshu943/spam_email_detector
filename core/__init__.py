"""
Core utilities package for Spam Email Detector

Modules:
- text_utils: Text processing and cleaning
- validation_utils: Input validation functions
- model_utils: ML model utilities
- gmail_utils: Gmail API integration
"""

from .text_utils import (
    transform_text,
    clean_html,
    clean_text_for_display,
    clean_text_for_model,
    extract_links,
)

from .validation_utils import (
    validate_text_input,
    validate_email_data,
    validate_batch_emails,
)

from .model_utils import (
    load_models,
    predict_spam,
)

from .gmail_utils import (
    gmail_authenticate,
    fetch_emails,
    extract_email_content,
)

__all__ = [
    # Text utilities
    "transform_text",
    "clean_html",
    "clean_text_for_display",
    "clean_text_for_model",
    "extract_links",
    # Validation utilities
    "validate_text_input",
    "validate_email_data",
    "validate_batch_emails",
    # Model utilities
    "load_models",
    "predict_spam",
    # Gmail utilities
    "gmail_authenticate",
    "fetch_emails",
    "extract_email_content",
]
