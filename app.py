from flask import Flask, request
from flask_cors import CORS
import requests
from chatbot import valaszolo_bot, hasonlo  # hasonlo is kell a gombos döntéshez
import os

app = Flask(__name__)
CORS(app, origins=["https://karitativ.hu"])

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


def send_quick_reply(recipient_id, message_text, quick_replies):
    url = "https://graph.facebook.com/v17.0/me/messages"
    headers = {"Content-Type": "application/json"}
    params = {"access_token": PAGE_ACCESS_TOKEN}
    data = {
        "recipient": {"id": recipient_id},
        "message": {
            "text": message_text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": reply,
                    "payload": reply
                } for reply in quick_replies
            ]
        }
    }
    response = requests.post(url, params=params, headers=headers, json=data)
    print("Quick reply küldve:", response.status_code, response.text)


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

                    print("Sender ID:", sender_id)

                    if message_text:
                        # 🔍 Ha üdvözlés → gombos válasz
                        if hasonlo(message_text, ["szia", "hello", "üdv"]):
                            send_quick_reply(sender_id, "Szia! Miben segíthetek? 😊", [
                                "Hol van ételosztás?",
                                "Szeretnék csomagot",
                                "Segítenék önkéntesként"
                            ])
                        else:
                            valasz = valaszolo_bot(message_text)
                            print("Bot válasz:", valasz)

                            # ha nem szám az ID → webes kérés
                            if not sender_id.isdigit():
                                response_text = valasz
                            else:
                                send_message(sender_id, valasz)
    except Exception as e:
        print("Hiba:", e)

    return response_text, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
