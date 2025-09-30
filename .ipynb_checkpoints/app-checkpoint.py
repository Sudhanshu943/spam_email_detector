import os
import re
import base64
import pickle
import streamlit as st
import nltk
import string
from html import unescape
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

nltk.download('punkt')
nltk.download('stopwords')

st.set_page_config(
    page_title="Spam Email Classifier",
    page_icon="📧",
    layout="wide"
)

# Configuration
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
EMAILS_PER_PAGE = 10

# Initialize NLTK components
@st.cache_resource
def init_nltk():
    """Initialize NLTK components with caching"""
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
    
    return PorterStemmer(), set(stopwords.words("english"))

ps, stop_words = init_nltk()

# Load ML models
@st.cache_resource
def load_models():
    """Load vectorizer and model with caching"""
    try:
        tfidf = pickle.load(open("models/vectorizer.pkl", "rb"))
        model = pickle.load(open("models/model.pkl", "rb"))
        return tfidf, model
    except FileNotFoundError as e:
        st.error(f"Model files not found in 'models/' folder: {e}")
        st.stop()
        return None, None  # Ensure function always returns a tuple

tfidf, model = load_models()


def transform_text(text):
    """Preprocess text for model prediction"""
    if not text:
        return ""
    
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [word for word in text if word.isalnum()]
    text = [word for word in text if word not in stop_words and word not in string.punctuation]
    text = [ps.stem(word) for word in text]
    return " ".join(text)

def gmail_authenticate():
    """Authenticate with Gmail API"""
    creds = None
    creds_path = os.path.join("config", "credentials.json")
    token_path = os.path.join("config", "token.json")

    # Load existing credentials
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                st.error("config/credentials.json file not found. Please add your Google API credentials.")
                st.stop()
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    
    return build("gmail", "v1", credentials=creds)

def extract_email_content(payload):
    """Extract plain text content from email payload"""
    def decode_part(part):
        """Decode a message part"""
        if "data" in part.get("body", {}):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")
        return ""
    
    # Direct body content
    if "body" in payload and payload["body"].get("data"):
        content = decode_part(payload)
        if payload.get("mimeType", "").startswith("text/html"):
            return clean_html(content)
        return content
    
    # Multipart content
    if "parts" in payload:
        # First try to find plain text
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
                return decode_part(part)
        
        # Fall back to HTML
        for part in payload["parts"]:
            if part.get("mimeType", "").startswith("text/html") and part.get("body", {}).get("data"):
                return clean_html(decode_part(part))
        
        # Recursively check nested parts
        for part in payload["parts"]:
            if "parts" in part:
                result = extract_email_content(part)
                if result:
                    return result
    
    return ""

def clean_html(html_content):
    """Convert HTML to plain text"""
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", html_content)
    # Decode HTML entities
    text = unescape(text)
    return text

def clean_text_for_display(text):
    """Clean text for display purposes"""
    if not text:
        return text
    
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def clean_text_for_model(text):
    """Clean text for model processing"""
    if not text:
        return text
    
    # Remove URLs
    text = re.sub(r"http[s]?://\S+", " ", text)
    text = re.sub(r"www\.\S+", " ", text)
    
    # Remove data URLs and CID references
    text = re.sub(r"data:image\/[^;]+;base64,[A-Za-z0-9+/=]+", " ", text)
    text = re.sub(r"cid:[^\s'\"<>]+", " ", text, flags=re.IGNORECASE)
    
    # Remove remaining HTML tags
    text = re.sub(r"<[^>]*>", " ", text, flags=re.IGNORECASE)
    
    # Clean whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_links(text):
    """Extract HTTP/HTTPS links from text"""
    if not text:
        return []
    return re.findall(r"http[s]?://\S+", text)

@st.cache_data
def fetch_emails(page_token=None, max_results=EMAILS_PER_PAGE):
    """Fetch emails from Gmail with caching"""
    try:
        service = gmail_authenticate()
        
        results = service.users().messages().list(
            userId="me",
            maxResults=max_results,
            pageToken=page_token
        ).execute()
        
        messages = results.get("messages", [])
        next_page_token = results.get("nextPageToken")
        
        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(
                userId="me", 
                id=msg["id"], 
                format="full"
            ).execute()
            
            # Extract headers
            headers = {h["name"]: h["value"] for h in msg_data.get("payload", {}).get("headers", [])}
            
            # Extract content
            raw_content = extract_email_content(msg_data.get("payload", {}))
            
            emails.append({
                "subject": headers.get("Subject", "No Subject"),
                "sender": headers.get("From", "Unknown Sender"),
                "date": headers.get("Date", "Unknown Date"),
                "raw_content": clean_text_for_display(raw_content),
                "cleaned_content": clean_text_for_model(raw_content),
                "links": extract_links(raw_content)
            })
        
        return emails, next_page_token
        
    except Exception as e:
        st.error(f"Error fetching emails: {e}")
        return [], None

def predict_spam(text):
    """Predict if text is spam"""
    if not text.strip():
        return None, 0.0
    
    transformed = transform_text(text)
    if not transformed:
        return None, 0.0
    
    vector_input = tfidf.transform([transformed])
    prediction = model.predict(vector_input)[0]
    probability = model.predict_proba(vector_input)[0].max()
    
    return prediction, probability

def initialize_session_state():
    """Initialize session state variables"""
    if "page_token_stack" not in st.session_state:
        st.session_state.page_token_stack = [None]
    if "current_page_index" not in st.session_state:
        st.session_state.current_page_index = 0


def main():
    """Main application"""
    st.title("📧 Spam Email Classifier")
    st.markdown("---")
    
    initialize_session_state()
    
    # Sidebar navigation
    menu = st.sidebar.radio(
        "Navigation",
        ["📨 Gmail Analysis", "✍️ Manual Text Check"],
        index=0
    )
    
    if menu == "📨 Gmail Analysis":
        gmail_analysis_page()
    else:
        manual_text_page()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Created by:** Sudhanshu Thapa")


def gmail_analysis_page():
    """Gmail analysis page"""
    st.header("📨 Gmail Spam Analysis")
    
    # Get current page token
    current_token = st.session_state.page_token_stack[st.session_state.current_page_index]
    
    # Fetch emails
    with st.spinner("Fetching emails..."):
        emails, next_token = fetch_emails(page_token=current_token)
    
    if not emails:
        st.warning("No emails found or unable to fetch emails.")
        return
    
    # Display summary
    st.info(f"Analyzing {len(emails)} emails (Page {st.session_state.current_page_index + 1})")
    
    # Analyze emails
    spam_count = 0
    for idx, email in enumerate(emails):
        prediction, confidence = predict_spam(email["cleaned_content"])
        
        if prediction == 1:
            spam_count += 1
            status = "🚨 **SPAM**"
            color = "red"
        elif prediction == 0:
            status = "✅ **SAFE**"
            color = "green"
        else:
            status = "⚠️ **UNABLE TO CLASSIFY**"
            color = "orange"
        
        # Display email card
        with st.expander(
            f"{status} | 📧 {email['subject'][:50]}{'...' if len(email['subject']) > 50 else ''}",
            expanded=(idx == 0)
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**From:** {email['sender']}")
                st.markdown(f"**Date:** {email['date']}")
                if prediction is not None:
                    st.markdown(f"**Confidence:** {confidence:.2%}")
            
            with col2:
                if email["links"]:
                    st.markdown("**🔗 Links Found:**")
                    for link in email["links"][:3]:  # Show max 3 links
                        st.markdown(f"• [{link[:30]}...]({link})")
                    if len(email["links"]) > 3:
                        st.markdown(f"• ... and {len(email['links']) - 3} more")
            
            st.markdown("**Email Content:**")
            content_preview = email["raw_content"][:500]
            if len(email["raw_content"]) > 500:
                content_preview += "..."
            st.text_area("", content_preview, height=100, key=f"email_{idx}")
    
    # Display statistics
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Emails", len(emails))
    with col2:
        st.metric("Spam Detected", spam_count, delta=f"{spam_count/len(emails):.1%}")
    with col3:
        st.metric("Safe Emails", len(emails) - spam_count, delta=f"{(len(emails)-spam_count)/len(emails):.1%}")
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_page_index > 0:
            if st.button("⬅️ Previous"):
                st.session_state.current_page_index -= 1
                st.rerun()
        else:
            st.button("⬅️ Previous", disabled=True)
    
    with col3:
        if next_token and st.button("Next ➡️"):
            # Add next token if moving forward for first time
            if st.session_state.current_page_index == len(st.session_state.page_token_stack) - 1:
                st.session_state.page_token_stack.append(next_token)
            st.session_state.current_page_index += 1
            st.rerun()

def manual_text_page():
    """Manual text analysis page"""
    st.header("✍️ Manual Text Classification")
    
    # Text input
    input_text = st.text_area(
        "Enter text to classify:",
        height=150,
        placeholder="Paste your email content or message here..."
    )
    
    # Analysis button
    if st.button("🔍 Analyze Text", type="primary"):
        if not input_text.strip():
            st.warning("Please enter some text to analyze!")
            return
        
        with st.spinner("Analyzing text..."):
            # Clean text for model
            cleaned_text = clean_text_for_model(input_text)
            prediction, confidence = predict_spam(cleaned_text)
        
        if prediction is None:
            st.warning("Unable to classify the text. Please try with different content.")
            return
        
        # Display results
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        if prediction == 1:
            st.error("🚨 **SPAM DETECTED**")
            st.markdown(f"**Confidence:** {confidence:.2%}")
        else:
            st.success("✅ **TEXT APPEARS SAFE**")
            st.markdown(f"**Confidence:** {confidence:.2%}")
        
        # Show extracted links if any
        links = extract_links(input_text)
        if links:
            st.subheader("🔗 Links Found:")
            for link in links:
                st.markdown(f"• {link}")
        
        # Text statistics
        st.subheader("📈 Text Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Characters", len(input_text))
        with col2:
            st.metric("Words", len(input_text.split()))
        with col3:
            st.metric("Links", len(links))

if __name__ == "__main__":
    main()