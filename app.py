from flask import Flask, request
from flask_cors import CORS
import requests
from chatbot import valaszolo_bot

app = Flask(__name__)
CORS(app, origins=["https://karitativ.hu"])

import os
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "lokalis_token")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "lokalis_page_token")

def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v17.0/me/messages"
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, params=params, headers=headers, json=data)
    print("Válasz elküldve:", response.status_code, response.text)

@app.route("/", methods=["GET"])
def webhook_verification():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("KAPTUNK:", data)

    response_text = "ok"

    try:
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender'].get('id', '')
                    message_text = messaging_event['message'].get('text')

                    print("Sender ID:", sender_id)  # <-- EZ LOGOL

                    if message_text:
                        valasz = valaszolo_bot(message_text)
                        print("Bot válasz:", valasz)

                        # ha nem szám az ID → webes kérés, küldjünk választ vissza
                        if not sender_id.isdigit():
                            response_text = valasz
                        else:
                            send_message(sender_id, valasz)
    except Exception as e:
        print("Hiba:", e)

    return response_text, 200

import os

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
