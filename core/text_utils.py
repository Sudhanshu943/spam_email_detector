"""
Text processing and cleaning utilities for Spam Email Detector
"""

import re
import string
import nltk
from html import unescape
from typing import List, Tuple
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

try:
    from ..logger import log_debug, log_warning
except ImportError:
    from logger import log_debug, log_warning

ps = PorterStemmer()
stop_words = set(stopwords.words("english"))


def transform_text(text: str) -> str:
    """Preprocess text for model prediction"""
    try:
        if not text:
            return ""
        
        text = text.lower()
        text = nltk.word_tokenize(text)
        text = [word for word in text if word.isalnum()]
        text = [word for word in text if word not in stop_words and word not in string.punctuation]
        text = [ps.stem(word) for word in text]
        log_debug("Text transformed successfully")
        return " ".join(text)
    except Exception as e:
        log_warning(f"Error transforming text: {e}")
        return ""


def clean_html(html_content: str) -> str:
    """Convert HTML to plain text"""
    try:
        text: str = re.sub(r"<[^>]+>", " ", html_content)
        text = unescape(text)
        log_debug("HTML cleaned successfully")
        return text
    except Exception as e:
        log_warning(f"Error cleaning HTML: {e}")
        return html_content


def clean_text_for_display(text: str) -> str:
    """Clean text for display purposes"""
    try:
        if not text:
            return text
        
        text = re.sub(r"\s+", " ", text).strip()
        return text
    except Exception as e:
        log_warning(f"Error cleaning text for display: {e}")
        return text


def clean_text_for_model(text: str) -> str:
    """Clean text for model processing"""
    try:
        if not text:
            return text
        
        text = re.sub(r"http[s]?://\S+", " ", text)
        text = re.sub(r"www\.\S+", " ", text)
        
        text = re.sub(r"data:image\/[^;]+;base64,[A-Za-z0-9+/=]+", " ", text)
        text = re.sub(r"cid:[^\s'\"<>]+", " ", text, flags=re.IGNORECASE)
        
        text = re.sub(r"<[^>]*>", " ", text, flags=re.IGNORECASE)
        
        text = re.sub(r"\s+", " ", text).strip()
        log_debug("Text cleaned for model successfully")
        return text
    except Exception as e:
        log_warning(f"Error cleaning text for model: {e}")
        return text


def extract_links(text: str) -> List[str]:
    """Extract HTTP/HTTPS links from text"""
    try:
        if not text:
            return []
        links = re.findall(r"http[s]?://\S+", text)
        log_debug(f"Extracted {len(links)} links from text")
        return links
    except Exception as e:
        log_warning(f"Error extracting links: {e}")
        return []
