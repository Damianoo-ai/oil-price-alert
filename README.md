# 📈 Oil Price Alert System

This project monitors crude oil prices and sends an SMS alert when the price changes by more than a defined threshold (e.g. ±5%).

When triggered, it:
- fetches recent news about oil markets
- filters relevant articles
- sends SMS notifications using Twilio

---

## ⚙️ Requirements

You need API keys for:

- NewsAPI
- Twilio

Yahoo Finance data is retrieved using `yfinance` (no API key required).

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
