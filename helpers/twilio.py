import os
from twilio.rest import Client

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

def send_twilio_message(to, from_, message):
    try:
        message = client.messages.create(
            body=message,
            from_=from_,
            to=to
        )

        # print('Message SID:', message.sid)
        # print('Response Body:', message.body)  

        return message.body

    except Exception as e:
        print(f"Error sending message: {e}")
        return {"message": "Message failed to send"}, 500

