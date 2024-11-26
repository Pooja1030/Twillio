# utils.py
from twilio.rest import Client
from django.conf import settings  # Imported settings to access environment variables
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_sms(phone_number, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)  # Using environment variables
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,  # Using environment variables
        to=phone_number
    )
    return message.sid

def send_otp_via_whatsapp(phone_number, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)  # Using environment variables
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=settings.TWILIO_WHATSAPP_NUMBER,  # Using environment variables
        to=f"whatsapp:{phone_number}"
    )
    return message.sid
