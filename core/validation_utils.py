"""
Input validation utilities for Spam Email Detector
"""

from typing import Tuple, Dict, List

try:
    from ..config import TEXT_VALIDATION, EMAIL_VALIDATION
    from ..logger import log_debug, log_warning
except ImportError:
    from config import TEXT_VALIDATION, EMAIL_VALIDATION
    from logger import log_debug, log_warning


def validate_text_input(text: str, min_length: int = TEXT_VALIDATION["min_length"], max_length: int = TEXT_VALIDATION["max_length"]) -> Tuple[bool, str]:
    """
    Validate text input for processing
    
    Args:
        text: Text to validate
        min_length: Minimum text length required
        max_length: Maximum text length allowed
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        if not isinstance(text, str):
            log_warning("Text validation failed: input is not a string")
            return False, "Text must be a string"
        
        if len(text.strip()) < min_length:
            log_warning(f"Text validation failed: text length {len(text.strip())} < {min_length}")
            return False, f"Text must contain at least {min_length} character(s)"
        
        if len(text) > max_length:
            log_warning(f"Text validation failed: text length {len(text)} > {max_length}")
            return False, f"Text exceeds maximum length of {max_length} characters"
        
        if text.strip() == "":
            log_warning("Text validation failed: text is empty or whitespace only")
            return False, "Text cannot be empty or contain only whitespace"
        
        log_debug("Text validation passed")
        return True, ""
    except Exception as e:
        log_warning(f"Error during text validation: {e}")
        return False, f"Validation error: {str(e)}"


def validate_email_data(email: Dict[str, str]) -> Tuple[bool, str]:
    """
    Validate email data structure
    
    Args:
        email: Email dictionary to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        required_fields = ["subject", "sender", "raw_content", "cleaned_content"]
        
        if not isinstance(email, dict):
            log_warning("Email validation failed: input is not a dictionary")
            return False, "Email must be a dictionary"
        
        for field in required_fields:
            if field not in email:
                log_warning(f"Email validation failed: missing field {field}")
                return False, f"Email missing required field: {field}"
            
            if field in ["subject", "sender", "raw_content", "cleaned_content"]:
                if not isinstance(email[field], str):
                    log_warning(f"Email validation failed: field {field} is not a string")
                    return False, f"Field '{field}' must be a string"
        
        if len(email.get("raw_content", "")) > EMAIL_VALIDATION["max_size"]:
            log_warning(f"Email validation failed: content size exceeds {EMAIL_VALIDATION['max_size']}")
            return False, "Email content exceeds maximum size"
        
        log_debug("Email validation passed")
        return True, ""
    except Exception as e:
        log_warning(f"Error during email validation: {e}")
        return False, f"Validation error: {str(e)}"


def validate_batch_emails(emails: List[Dict]) -> Tuple[bool, str, List[Dict]]:
    """
    Validate a batch of emails
    
    Args:
        emails: List of email dictionaries
    
    Returns:
        Tuple of (is_valid, error_message, valid_emails)
    """
    try:
        if not isinstance(emails, list):
            log_warning("Batch validation failed: input is not a list")
            return False, "Emails must be a list", []
        
        if len(emails) == 0:
            log_warning("Batch validation failed: empty email list")
            return False, "No emails provided", []
        
        valid_emails = []
        invalid_count = 0
        
        for idx, email in enumerate(emails):
            is_valid, error_msg = validate_email_data(email)
            if is_valid:
                valid_emails.append(email)
            else:
                invalid_count += 1
        
        if invalid_count > 0 and len(valid_emails) == 0:
            log_warning(f"Batch validation failed: all {invalid_count} emails invalid")
            return False, f"All {invalid_count} emails failed validation", []
        
        if invalid_count > 0:
            message = f"Validated {len(valid_emails)} email(s), skipped {invalid_count} invalid email(s)"
            log_debug(message)
            return True, message, valid_emails
        
        log_debug(f"Batch validation passed: {len(valid_emails)} emails valid")
        return True, "", valid_emails
    except Exception as e:
        log_warning(f"Error during batch validation: {e}")
        return False, f"Validation error: {str(e)}", []
