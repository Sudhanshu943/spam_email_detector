# Spam Email Classifier

A machine learning based **Spam Email Classifier** that predicts whether an email is **Spam** or **Not Spam**.  
This project uses Natural Language Processing (NLP) techniques and a trained model to classify emails accurately.

---

## 🚀 Features

- Classifies emails as **Spam** or **Not Spam**.
- User-friendly web interface using **Streamlit**.
- Pre-trained ML model for fast predictions.
- Easy to run locally on your system.

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Streamlit** – for web interface
- **scikit-learn** – for machine learning model
- **pandas / numpy** – for data processing
- **NLTK** – for text preprocessing

---

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/spam-email-classifier.git
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

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and create pull requests.

---

## 📜 License

This project is licensed under the **MIT License**.
