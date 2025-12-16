"""
ML Model utilities for Spam Email Detector
"""

import pickle
import streamlit as st
from typing import Tuple, Optional
from config import PATHS, ERROR_MESSAGES
from logger import log_info, log_error, log_debug
from text_utils import transform_text
from validation_utils import validate_text_input
from config import TEXT_VALIDATION


def load_models() -> Tuple[Optional[object], Optional[object]]:
    """Load vectorizer and model with caching"""
    try:
        log_info("Loading ML models from disk...")
        with open(PATHS["vectorizer_file"], "rb") as f:
            tfidf = pickle.load(f)
        with open(PATHS["model_file"], "rb") as f:
            model = pickle.load(f)
        log_info("ML models loaded successfully")
        return tfidf, model
    except FileNotFoundError as e:
        log_error(f"{ERROR_MESSAGES['model_not_found']}", exception=e)
        st.error(f"{ERROR_MESSAGES['model_not_found']}: {e}")
        st.stop()
        return None, None
    except pickle.UnpicklingError as e:
        log_error("Corrupted pickle data in model files", exception=e)
        st.error(f"Error loading model files - corrupted pickle data: {e}")
        st.stop()
        return None, None
    except Exception as e:
        log_error("Unexpected error loading models", exception=e)
        st.error(f"Unexpected error loading models: {e}")
        st.stop()
        return None, None


def predict_spam(text: str, tfidf: object, model: object) -> Tuple[Optional[int], float]:
    """Predict if text is spam"""
    try:
        is_valid, error_msg = validate_text_input(text, min_length=TEXT_VALIDATION["min_length"], max_length=TEXT_VALIDATION["max_length"])
        if not is_valid:
            log_info(f"Text validation failed: {error_msg}")
            return None, 0.0
        
        log_debug("Starting spam prediction...")
        transformed = transform_text(text)
        if not transformed:
            log_info("Transformed text is empty")
            return None, 0.0
        
        try:
            vector_input = tfidf.transform([transformed])
            prediction = model.predict(vector_input)[0]
            probability = model.predict_proba(vector_input)[0].max()
            log_info(f"Prediction made: {prediction}, Confidence: {probability:.2%}")
            return prediction, probability
        except Exception as e:
            log_error(f"{ERROR_MESSAGES['prediction_error']}", exception=e)
            st.error(f"{ERROR_MESSAGES['prediction_error']}: {e}")
            return None, 0.0
    
    except Exception as e:
        log_error("Unexpected error in prediction", exception=e)
        st.error(f"Unexpected error in prediction: {e}")
        return None, 0.0
