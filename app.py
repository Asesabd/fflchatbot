from flask import Flask, request
from flask_cors import CORS
import requests
import os

from valaszolo_bot import valaszolo_bot

app = Flask(__name__)
CORS(app, origins=["https://karitativ.hu"])

# 🔐 Facebook API tokenek
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "lokalis_token")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "lokalis_page_token")

# 📤 Üzenetküldő függvény Facebookra
def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v17.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    response = requests.post(url, params=params, headers=headers, json=data)
    print("Válasz elküldve:", response.status_code, response.text)

# ✅ Render / uptime / ellenőrző endpoint
@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

# ✅ Facebook webhook hitelesítés (GET) + Render root ping (GET / paraméter nélkül)
@app.route("/", methods=["GET"])
def webhook_verification():
    # Facebook verify hívás query paraméterekkel
    verify_token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if verify_token is not None:
        if verify_token == VERIFY_TOKEN:
            return challenge or "", 200
        return "Invalid verification token", 403

    # Render / böngésző sima ping (paraméter nélkül)
    return "OK", 200

# 💬 Üzenet fogadás és válasz (POST)
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json() or {}
    print("📥 KAPTUNK:", data)

    try:
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event.get("sender", {}).get("id", "")
                message = event.get("message", {})
                message_text = (message.get("text") or "").strip()

                if message_text and sender_id:
                    print("👤 Feladó:", sender_id)

                    # ⚠️ fontos: legyen állapot per user
                    # (Messengerben egyszerre sok user van; különben összekeverednek)
                    if not hasattr(webhook, "states"):
                        webhook.states = {}
                    state = webhook.states.setdefault(sender_id, {"ag": None})

                    valasz = valaszolo_bot(message_text, state)
                    print("🤖 Válasz:", valasz)

                    if valasz and valasz != "exit":
                        send_message(sender_id, valasz)

    except Exception as e:
        print("❌ Hiba:", e)

    return "ok", 200

# 🚀 Lokális futtatás (Render gunicorn alatt ezt nem használja)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)