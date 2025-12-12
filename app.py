from flask import Flask, request
from flask_cors import CORS
import requests
import os

from valaszolo_bot import valaszolo_bot

app = Flask(__name__)
CORS(app, origins=["https://karitativ.hu"])

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "lokalis_token")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "lokalis_page_token")


def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v17.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {"recipient": {"id": recipient_id}, "message": {"text": message_text}}
    r = requests.post(url, params=params, headers=headers, json=data)
    print("Válasz elküldve:", r.status_code, r.text)


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


def handle_verification():
    verify_token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if verify_token is not None:
        if verify_token == VERIFY_TOKEN:
            return challenge or "", 200
        return "Invalid verification token", 403

    # sima ping
    return "OK", 200


def handle_webhook_post():
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

                    # állapot per user
                    if not hasattr(handle_webhook_post, "states"):
                        handle_webhook_post.states = {}
                    state = handle_webhook_post.states.setdefault(sender_id, {"ag": None})

                    valasz = valaszolo_bot(message_text, state)
                    print("🤖 Válasz:", valasz)

                    if valasz and valasz != "exit":
                        send_message(sender_id, valasz)

    except Exception as e:
        print("❌ Hiba:", e)

    return "ok", 200


# ✅ FACEBOOK CALLBACK ROOTON
@app.route("/", methods=["GET"])
def root_get():
    return handle_verification()

@app.route("/", methods=["POST"])
def root_post():
    return handle_webhook_post()


# ✅ OPCIONÁLIS: ha később mégis engednék /webhook-kal
@app.route("/webhook", methods=["GET"])
def webhook_get():
    return handle_verification()

@app.route("/webhook", methods=["POST"])
def webhook_post():
    return handle_webhook_post()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)