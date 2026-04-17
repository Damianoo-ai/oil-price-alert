# 📈 Oil Price Alert System

This project monitors crude oil prices and sends SMS alerts when significant price movements occur.

When a threshold is reached, it:
- retrieves recent financial news related to oil markets  
- filters the most relevant articles  
- sends SMS notifications via Twilio  

---

## ⚙️ Requirements

The project uses external APIs. You need API keys for:

- NewsAPI
- Twilio

Price data is retrieved using `yfinance` (no API key required).

---

## 🔐 Environment variables

Create a `.env` file based on `.env.example`:
NEWS_API_KEY=
BITLY_TOKEN=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_TRIAL_NUMBER=
TEST_NUMBER=

---

## ▶️ How to run
python main.py

---

## ⚠️ Notes

The project will not work without valid API keys configured.
