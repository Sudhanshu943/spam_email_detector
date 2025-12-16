# Spam Email Detector

A professional machine learning-based application for detecting spam emails using Gmail API integration and advanced text processing techniques.

## 📁 Project Structure

```
spam_email_detector/
├── app.py                          # Main application (original)
├── config.py                       # Configuration settings
├── logger.py                       # Logging system
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
│
├── core/                           # Core utilities (ORGANIZED MODULES)
│   ├── __init__.py                 # Module init
│   ├── text_utils.py              # Text processing functions
│   ├── validation_utils.py        # Input validation
│   ├── model_utils.py             # ML model utilities
│   └── gmail_utils.py             # Gmail API utilities
│
├── models/                         # Machine Learning Models
│   ├── spam_email_model.ipynb     # Jupyter notebook (model training)
│   ├── vectorizer.pkl             # TF-IDF vectorizer (trained)
│   └── model.pkl                  # Spam detection model
│
├── config/                         # Configuration & Credentials
│   ├── credentials.json           # Google OAuth credentials (ADD YOUR OWN)
│   └── token.json                 # Gmail API token (auto-generated)
│
├── dataset/                        # Training Data
│   └── spam.csv                   # Email dataset (training data)
│
└── logs/                           # Application Logs (auto-created)
    └── app.log                    # Detailed application logs
```

## 🚀 Features

- ✅ **Gmail Integration** - Real-time email analysis
- ✅ **ML Model** - Advanced spam detection
- ✅ **Text Processing** - Sophisticated NLP techniques
- ✅ **Input Validation** - Robust validation system
- ✅ **Error Handling** - Comprehensive error recovery
- ✅ **Logging System** - Detailed application logs
- ✅ **Type Hints** - Full type annotations
- ✅ **Modular Code** - Clean, organized structure
- ✅ **Configuration** - Centralized settings

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** – Web interface
- **scikit-learn** – ML models
- **NLTK** – NLP processing
- **Google API** – Gmail integration
- **Pandas** – Data processing

## 📋 Installation

### Prerequisites

```bash
python --version  # Python 3.8+
pip --version     # pip package manager
```

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Setup Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download JSON and save as `config/credentials.json`

### Step 3: Run Application

```bash
streamlit run app_new.py
```

## 🎯 Usage

### Option 1: Gmail Analysis

1. Open app → Click "📨 Gmail Analysis"
2. App fetches and analyzes your recent emails
3. See spam/safe classification with confidence score
4. Navigate through pages

### Option 2: Manual Text Check

1. Open app → Click "✍️ Manual Text Check"
2. Paste email content or text
3. Click "🔍 Analyze Text"
4. Get instant classification

## 📚 Core Modules

### `text_utils.py`

- `transform_text()` - Tokenize and preprocess
- `clean_html()` - HTML to plain text
- `clean_text_for_display()` - Format for UI
- `clean_text_for_model()` - Prepare for ML
- `extract_links()` - Extract URLs

### `validation_utils.py`

- `validate_text_input()` - Validate text
- `validate_email_data()` - Validate email structure
- `validate_batch_emails()` - Validate multiple emails

### `model_utils.py`

- `load_models()` - Load pre-trained models
- `predict_spam()` - Make predictions

### `gmail_utils.py`

- `gmail_authenticate()` - OAuth authentication
- `fetch_emails()` - Get emails from Gmail
- `extract_email_content()` - Extract email body

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Limits
EMAILS_PER_PAGE = 10

# Text validation
TEXT_VALIDATION = {
    "min_length": 1,
    "max_length": 100000,
}

# UI settings
UI_CONFIG = {
    "page_title": "Spam Email Detector",
    "preview_length": 500,
}
```

## 📊 Model Training

Train new model:

1. Open `models/spam_email_model.ipynb`
2. Run all cells in Jupyter
3. Models saved as pickle files

## 📝 Logging

Logs automatically saved to `logs/app.log`:

- **INFO** - General information
- **WARNING** - Warning messages
- **ERROR** - Errors with details
- **DEBUG** - Debugging information

View logs:

```bash
tail -f logs/app.log  # Linux/Mac
Get-Content logs/app.log -Tail 20  # PowerShell
```

## 🔍 Troubleshooting

| Issue                 | Solution                                         |
| --------------------- | ------------------------------------------------ |
| Model files not found | Train models using Jupyter notebook              |
| Gmail auth failed     | Check credentials.json and Gmail API enabled     |
| No emails found       | Ensure account connected and has emails          |
| NLTK error            | Run: `python -m nltk.downloader punkt stopwords` |

## 📈 Code Quality Improvements

1. ✅ Error Handling - Try-catch blocks everywhere
2. ✅ Input Validation - All inputs validated
3. ✅ Type Hints - Full annotations
4. ✅ Configuration - Centralized settings
5. ✅ Logging - Detailed logging system
6. ✅ Modularization - Clean code structure

## 🎓 Learning Path

1. **Understand Config** - Read `config.py`
2. **Study Core Modules** - Check `core/` folder
3. **Review Main App** - Read `app_new.py`
4. **Train Models** - Run Jupyter notebook
5. **Deploy** - Run application

## 📦 Requirements

```
streamlit==1.28.0
nltk==3.8.1
scikit-learn==1.3.2
pandas==2.1.1
numpy==1.26.0
seaborn==0.12.2
matplotlib==3.8.0
google-auth==2.22.0
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.0
google-api-python-client==2.88.0
```

## 👨‍💻 Created By

1. Sudhanshu Thapa
2. Raj Pratap Singh
3. Chris Joshi

---

**Last Updated**: December 2025 ✨

- **scikit-learn** – for machine learning model
- **pandas / numpy** – for data processing
- **NLTK** – for text preprocessing

---

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Sudhanshu943/spam_email_detector.git
   cd spam-email-classifier
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**

   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

1. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. Open browser and go to:

   ```
   http://localhost:8501
   ```

3. Paste your email text in the input box → Click **Predict** → Get result (**Spam / Not Spam**).

---

## 📂 Project Structure

```
spam-email-classifier/
│
├── dataset/                # Email dataset
│ └── spam.cvs
├── models/                 # Model training & storage
│ ├── spam_email_model.py
│ ├── model.pkl
│ └── vectorizer.pk
├── config/                 # Configuration & credentials
│   ├── credentials.json    # Google OAuth credentials (downloaded from Google Cloud Console)
│   └── token.json          # Generated after first authentication (OAuth tokens)
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── README.md               # Documentation

```

---

## 📝 Requirements

- Python 3.8+
- Required Python libraries (install from `requirements.txt`)

---

## 📌 Future Improvements

- Improve accuracy with deep learning (LSTM/BERT).
- Add support for multiple languages.
- Deploy on cloud (Heroku/Streamlit Cloud).

---

## 📜 License

This project is licensed under the **Thapa Company License**.
