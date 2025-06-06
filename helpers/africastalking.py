import os
import africastalking

africastalking.initialize(
    username=os.environ.get("AFRICASTALKING_USERNAME"),
    api_key=os.environ.get("AFRICASTALKING_API_KEY"),
)

class AfricasTalking:
    sms = africastalking.SMS
    def send(self, sender, message, recipients):
        try:
            response = self.sms.send(message, recipients, sender)
            return response
        except Exception as e:
            print(f"Houston, we have a problem: {e}")
            return {"message":"Message failed to send"}, 500
