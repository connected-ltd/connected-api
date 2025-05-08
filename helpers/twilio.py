# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

def send_twilio_message(to, from_, message):
    print("Received message from:", from_)
    print("Sending message to:", to)
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
        print("Not Working")
        print(f"Error sending message: {e}")
        return {"message": "Message failed to send"}, 500

