"""
Spam Email Detector - Main Application
Streamlit-based web application for detecting spam emails
"""

import streamlit as st
from typing import Optional
from config import UI_CONFIG, EMAILS_PER_PAGE
from logger import log_info, log_warning
from core.model_utils import load_models, predict_spam
from core.gmail_utils import fetch_emails
from core.text_utils import clean_text_for_model, extract_links

st.set_page_config(
    page_title=UI_CONFIG["page_title"],
    page_icon=UI_CONFIG["page_icon"],
    layout=UI_CONFIG["layout"]
)

tfidf, model = load_models()


def initialize_session_state() -> None:
    """Initialize session state variables"""
    if "page_token_stack" not in st.session_state:
        st.session_state.page_token_stack = [None]
    if "current_page_index" not in st.session_state:
        st.session_state.current_page_index = 0


def main() -> None:
    """Main application"""
    log_info("Application started")
    st.title("📧 Spam Email Detector")
    st.markdown("---")
    
    initialize_session_state()
    
    menu = st.sidebar.radio(
        "Navigation",
        ["📨 Gmail Analysis", "✍️ Manual Text Check"],
        index=0
    )
    
    if menu == "📨 Gmail Analysis":
        gmail_analysis_page()
    else:
        manual_text_page()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Created by:**\n1. Sudhanshu Thapa\n2. Raj Pratap Singh\n3. Chris Joshi")


def gmail_analysis_page() -> None:
    """Gmail analysis page"""
    log_info("User navigated to Gmail Analysis page")
    st.header("📨 Gmail Spam Analysis")
    
    current_token = st.session_state.page_token_stack[st.session_state.current_page_index]
    
    with st.spinner("Fetching emails..."):
        emails, next_token = fetch_emails(page_token=current_token)
    
    if not emails:
        st.warning("No emails found or unable to fetch emails.")
        return
    
    st.info(f"Analyzing {len(emails)} emails (Page {st.session_state.current_page_index + 1})")
    
    spam_count = 0
    for idx, email in enumerate(emails):
        prediction, confidence = predict_spam(email["cleaned_content"], tfidf, model)
        
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
                    for link in email["links"][:UI_CONFIG["max_links_display"]]:
                        st.markdown(f"• [{link[:30]}...]({link})")
                    if len(email["links"]) > UI_CONFIG["max_links_display"]:
                        st.markdown(f"• ... and {len(email['links']) - UI_CONFIG['max_links_display']} more")
            
            st.markdown("**Email Content:**")
            content_preview = email["raw_content"][:UI_CONFIG["preview_length"]]
            if len(email["raw_content"]) > UI_CONFIG["preview_length"]:
                content_preview += "..."
            st.text_area("", content_preview, height=100, key=f"email_{idx}")
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Emails", len(emails))
    with col2:
        st.metric("Spam Detected", spam_count, delta=f"{spam_count/len(emails):.1%}")
    with col3:
        st.metric("Safe Emails", len(emails) - spam_count, delta=f"{(len(emails)-spam_count)/len(emails):.1%}")
    
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
            if st.session_state.current_page_index == len(st.session_state.page_token_stack) - 1:
                st.session_state.page_token_stack.append(next_token)
            st.session_state.current_page_index += 1
            st.rerun()


def manual_text_page() -> None:
    """Manual text analysis page"""
    log_info("User navigated to Manual Text Check page")
    st.header("✍️ Manual Text Classification")
    
    input_text = st.text_area(
        "Enter text to classify:",
        height=150,
        placeholder="Paste your email content or message here..."
    )
    
    if st.button("🔍 Analyze Text", type="primary"):
        if not input_text.strip():
            st.warning("Please enter some text to analyze!")
            return
        
        with st.spinner("Analyzing text..."):
            cleaned_text = clean_text_for_model(input_text)
            prediction, confidence = predict_spam(cleaned_text, tfidf, model)
        
        if prediction is None:
            st.warning("Unable to classify the text. Please try with different content.")
            return
        
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        if prediction == 1:
            st.error("🚨 **SPAM DETECTED**")
            st.markdown(f"**Confidence:** {confidence:.2%}")
        else:
            st.success("✅ **TEXT APPEARS SAFE**")
            st.markdown(f"**Confidence:** {confidence:.2%}")
        
        links = extract_links(input_text)
        if links:
            st.subheader("🔗 Links Found:")
            for link in links:
                st.markdown(f"• {link}")
        
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
