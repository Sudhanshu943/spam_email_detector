"""
Gmail API utilities for Spam Email Detector
"""

import os
import base64
import streamlit as st
from typing import Tuple, Dict, List, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import SCOPES, PATHS, ERROR_MESSAGES, EMAILS_PER_PAGE
from logger import log_info, log_warning, log_error, log_debug
from text_utils import clean_text_for_display, clean_text_for_model, extract_links
from validation_utils import validate_email_data


def gmail_authenticate() -> object:
    """Authenticate with Gmail API"""
    creds: Optional[Credentials] = None
    creds_path: str = PATHS["credentials_file"]
    token_path: str = PATHS["token_file"]

    try:
        log_info("Starting Gmail authentication process...")
        if os.path.exists(token_path):
            try:
                log_debug("Loading credentials from token file...")
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
                log_info("Credentials loaded from token file")
            except Exception as e:
                log_warning(f"Token file corrupted or expired: {e}")
                st.warning(f"Token file corrupted or expired: {e}. Requesting new authorization.")
                creds = None
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    log_info("Refreshing expired credentials...")
                    creds.refresh(Request())
                    log_info("Credentials refreshed successfully")
                except Exception as e:
                    log_warning(f"Failed to refresh credentials: {e}")
                    st.warning(f"Failed to refresh credentials: {e}. Requesting new authorization.")
                    creds = None
            
            if not creds:
                if not os.path.exists(creds_path):
                    log_error(ERROR_MESSAGES["credentials_not_found"])
                    st.error(ERROR_MESSAGES["credentials_not_found"])
                    st.stop()
                try:
                    log_info("Requesting new authorization from user...")
                    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                    log_info("New authorization obtained successfully")
                except Exception as e:
                    log_error(f"{ERROR_MESSAGES['authentication_error']}", exception=e)
                    st.error(f"{ERROR_MESSAGES['authentication_error']}: {e}")
                    st.stop()
            
            try:
                os.makedirs(PATHS["config_dir"], exist_ok=True)
                with open(token_path, "w") as token:
                    token.write(creds.to_json())
                log_info("Credentials saved to token file")
            except Exception as e:
                log_warning(f"Could not save token file: {e}")
        
        try:
            service = build("gmail", "v1", credentials=creds)
            log_info("Gmail service built successfully")
            return service
        except Exception as e:
            log_error("Failed to build Gmail service", exception=e)
            st.error(f"Failed to build Gmail service: {e}")
            st.stop()
    
    except Exception as e:
        log_error("Unexpected error during authentication", exception=e)
        st.error(f"Unexpected error during authentication: {e}")
        st.stop()


def extract_email_content(payload: Dict) -> str:
    """Extract plain text content from email payload"""
    def decode_part(part: Dict) -> str:
        """Decode a message part"""
        try:
            if "data" in part.get("body", {}):
                return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")
            return ""
        except Exception as e:
            log_warning(f"Error decoding email part: {e}")
            return ""
    
    try:
        if "body" in payload and payload["body"].get("data"):
            content = decode_part(payload)
            if payload.get("mimeType", "").startswith("text/html"):
                return clean_html(content)
            return content
        
        if "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
                    return decode_part(part)
            
            for part in payload["parts"]:
                if part.get("mimeType", "").startswith("text/html") and part.get("body", {}).get("data"):
                    return clean_html(decode_part(part))
            
            for part in payload["parts"]:
                if "parts" in part:
                    result = extract_email_content(part)
                    if result:
                        return result
        
        return ""
    except Exception as e:
        log_warning(f"Error extracting email content: {e}")
        return ""


def clean_html(html_content: str) -> str:
    """Convert HTML to plain text"""
    try:
        import re
        from html import unescape
        text: str = re.sub(r"<[^>]+>", " ", html_content)
        text = unescape(text)
        log_debug("HTML cleaned successfully")
        return text
    except Exception as e:
        log_warning(f"Error cleaning HTML: {e}")
        return html_content


def fetch_emails(page_token: Optional[str] = None, max_results: int = EMAILS_PER_PAGE) -> Tuple[List[Dict], Optional[str]]:
    """Fetch emails from Gmail"""
    try:
        log_info(f"Fetching {max_results} emails from Gmail...")
        service = gmail_authenticate()
        
        try:
            results = service.users().messages().list(
                userId="me",
                maxResults=max_results,
                pageToken=page_token
            ).execute()
            log_info("Email list retrieved successfully")
        except Exception as e:
            log_error("Failed to fetch email list", exception=e)
            st.error(f"Failed to fetch email list: {e}")
            return [], None
        
        messages = results.get("messages", [])
        next_page_token = results.get("nextPageToken")
        log_debug(f"Retrieved {len(messages)} messages")
        
        emails = []
        for idx, msg in enumerate(messages):
            try:
                msg_data = service.users().messages().get(
                    userId="me", 
                    id=msg["id"], 
                    format="full"
                ).execute()
                
                headers = {h["name"]: h["value"] for h in msg_data.get("payload", {}).get("headers", [])}
                
                try:
                    raw_content = extract_email_content(msg_data.get("payload", {}))
                    log_debug(f"Extracted content from email {idx}")
                except Exception as e:
                    log_warning(f"Could not extract content from email {idx}: {e}")
                    st.warning(f"Could not extract content from email {idx}: {e}")
                    raw_content = ""
                
                email_data = {
                    "subject": headers.get("Subject", "No Subject"),
                    "sender": headers.get("From", "Unknown Sender"),
                    "date": headers.get("Date", "Unknown Date"),
                    "raw_content": clean_text_for_display(raw_content),
                    "cleaned_content": clean_text_for_model(raw_content),
                    "links": extract_links(raw_content)
                }
                
                is_valid, error_msg = validate_email_data(email_data)
                if is_valid:
                    emails.append(email_data)
                    log_debug(f"Email {idx} validated successfully")
                else:
                    log_warning(f"Email {idx} validation failed: {error_msg}")
                    st.warning(f"Email {idx} validation failed: {error_msg}")
                    
            except Exception as e:
                log_warning(f"Failed to process email {idx}: {e}")
                st.warning(f"Failed to process email {idx}: {e}")
                continue
        
        log_info(f"Successfully fetched and validated {len(emails)} emails")
        return emails, next_page_token
        
    except Exception as e:
        log_error(f"{ERROR_MESSAGES['email_fetch_error']}", exception=e)
        st.error(f"{ERROR_MESSAGES['email_fetch_error']}: {e}")
        return [], None
