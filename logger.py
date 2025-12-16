"""
Logging configuration for Spam Email Detector application
"""

import logging
import os
from datetime import datetime
from config import LOGGING_CONFIG

def setup_logger() -> logging.Logger:
    """
    Setup and configure logger for the application
    
    Returns:
        Configured logger instance
    """
    os.makedirs(LOGGING_CONFIG["log_dir"], exist_ok=True)
    
    logger = logging.getLogger("SpamEmailDetector")
    logger.setLevel(getattr(logging, LOGGING_CONFIG["level"]))
    
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler = logging.FileHandler(LOGGING_CONFIG["log_file"])
    file_handler.setLevel(getattr(logging, LOGGING_CONFIG["level"]))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logger()


def log_info(message: str) -> None:
    """Log info message"""
    logger.info(message)


def log_warning(message: str) -> None:
    """Log warning message"""
    logger.warning(message)


def log_error(message: str, exception: Exception = None) -> None:
    """Log error message with optional exception details"""
    if exception:
        logger.error(f"{message} - Exception: {str(exception)}", exc_info=True)
    else:
        logger.error(message)


def log_debug(message: str) -> None:
    """Log debug message"""
    logger.debug(message)
