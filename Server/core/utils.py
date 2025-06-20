import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_PHONE_NUMBER =''


def send_sms(to_phone, body):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.api.account.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=f"+91{to_phone}"
        )
        print(f"✅ SMS sent to {to_phone}: SID = {message.sid}")
    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")
