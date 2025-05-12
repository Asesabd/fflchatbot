from flask import Flask, request
import requests
from chatbot import valaszolo_bot

app = Flask(__name__)

VERIFY_TOKEN = "asesa_verify_123"
PAGE_ACCESS_TOKEN = "EAATXlHTQ8rEBOzoRsFiyVUkY4o9kOHjcOQtkHEqe6ZCGAaQss0ganywEFPIXZBiyIPXus45rLTMFi7SXWbOwJFsXskNLZBdOpFN8FSEYntU1UsTKiaMZAjEMpJpwUb0lHthWJ3DgJKhiQchYiYmFuYGrnhIJoVe203xINX1Bv0jF94zdDLAKXZBCOX7aWWL7jNSuG8rifUrsxSCkE"

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

    try:
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message'].get('text')
                    if message_text:
                        valasz = valaszolo_bot(message_text)
                        print("Bot válasz:", valasz)
                        send_message(sender_id, valasz)
    except Exception as e:
        print("Hiba:", e)

    return "ok", 200

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
