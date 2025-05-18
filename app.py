from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

#route

@app.route("/", methods=["POST"])
def receive_alert():
    data = request.get_json()
    message = data.get("message", "📈 New alert received!")

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    r = requests.post(telegram_url, json=payload)
    return {"telegram_status": r.status_code}, 200

