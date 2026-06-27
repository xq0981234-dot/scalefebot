import requests
import time
import os
from telegram import Bot
import google.generativeai as genai

# TELEGRAM
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

# GEMINI API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

SYMBOL = "BTCUSDT"

def get_price_data():
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval=1m&limit=50"
    return requests.get(url).json()

def analyze(data):
    prompt = f"""
You are a crypto scalping assistant.

Analyze this 1m Binance data:
{data}

Return ONLY:
- LONG / SHORT / NO TRADE
- Entry
- SL
- TP1 TP2 TP3
- Confidence (0-100)

Be strict. No weak trades.
"""

    response = model.generate_content(prompt)
    return response.text

def send(msg):
    bot.send_message(chat_id=CHAT_ID, text=msg)

while True:
    try:
        data = get_price_data()
        result = analyze(data)
        send(result)
        time.sleep(60)
    except Exception as e:
        send(f"Error: {e}")
        time.sleep(60)
