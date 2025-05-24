from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Load all bot tokens and chat IDs from environment
BOT1_TOKEN = os.getenv("BOT_TOKEN")       # default or 4h bot
BOT1_CHAT_ID = os.getenv("CHAT_ID")

BOT2_TOKEN = os.getenv("BOT2_TOKEN")      # 1h bot
BOT2_CHAT_ID = os.getenv("BOT2_CHAT_ID")

@app.route("/", methods=["POST"])
def receive_alert():
    data = request.get_json()
    message = data.get("message", "📈 New alert received!")

    # Ignore synthetic ping messages
    if message == "🛠️ Keep-alive ping from Datadog Synthetic":
        return {"telegram_status": "ping skipped"}, 200

    # Route based on message prefix
    if message.startswith("4h"):
        bot_token = BOT1_TOKEN
        chat_id = BOT1_CHAT_ID
    elif message.startswith("1h"):
        bot_token = BOT2_TOKEN
        chat_id = BOT2_CHAT_ID
    else:
        bot_token = BOT1_TOKEN
        chat_id = BOT1_CHAT_ID

    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    r = requests.post(telegram_url, json=payload)

    return {"telegram_status": r.status_code}, 200
