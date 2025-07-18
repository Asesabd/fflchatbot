from flask import Flask, request
from flask_cors import CORS
import requests
import os
from chatbot import valaszolo_bot  # számgombos logikát tartalmazza

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

# ✅ Facebook webhook hitelesítés (GET)
@app.route("/", methods=["GET"])
def webhook_verification():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token", 403

# 💬 Üzenet fogadás és válasz (POST)
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 KAPTUNK:", data)

    try:
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event.get("sender", {}).get("id", "")
                message = event.get("message", {})
                message_text = message.get("text", "").strip()

                if message_text:
                    print("👤 Feladó:", sender_id)
                    valasz = valaszolo_bot(message_text)
                    print("🤖 Válasz:", valasz)

                    # Csak akkor küldj vissza, ha nem "exit" a válasz
                    if valasz != "exit":
                        send_message(sender_id, valasz)
    except Exception as e:
        print("❌ Hiba:", e)

    return "ok", 200

# 🚀 Lokális futtatás
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
