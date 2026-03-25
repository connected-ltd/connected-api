import os
import httpx

hollatags_api = os.environ.get("HOLLATAGS_API_URL")

async def send_sms(user, password, sender, receiver, msg):
    payload = {
        "user": user,
        "pass": password,
        "from": sender,
        "to": receiver,
        "msg": msg
    }
    async with httpx.AsyncClient() as client:
        print(f"Sending payload to Hollatags API: {payload}")
        response = await client.post(f"{hollatags_api}/send", data=payload)
        response.raise_for_status()
    
    print(f"API Response text: '{response.text}'")
    print(f"API Response status: {response.status_code}")
    
    if response.text.lower() == "sent":
        return {"message": "SMS sent successfully", "status": "success"}
    else:
        return {"message": "Failed to send SMS", "status": "error", "details": response.text}