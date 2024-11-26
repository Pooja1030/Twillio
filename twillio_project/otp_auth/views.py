# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import UserProfile  
from .utils import generate_otp, send_otp_via_sms, send_otp_via_whatsapp  # No change in imports
from .serializers import OTPSerializer, VerifyOTPSerializer
from twilio.base.exceptions import TwilioRestException  
import logging
import time

User = get_user_model()

# dictionary to store OTP (key: phone_number, value: (otp, timestamp))
otp_storage = {}

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SendOTPView(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            # Generate OTP and timestamp
            otp = generate_otp()
            timestamp = time.time()

            # Storing the OTP and timestamp temporarily
            otp_storage[phone_number] = (otp, timestamp)

            # OTP generation
            logger.info(f"Generated OTP {otp} for phone number {phone_number}")

            try:
                # Send OTP via SMS and WhatsApp
                send_otp_via_sms(phone_number, otp)  # This uses the environment variables
                send_otp_via_whatsapp(phone_number, otp)  # This uses the environment variables

                return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
            except TwilioRestException as e:
                logger.error(f"Error sending OTP to {phone_number}: {e}")
                return Response({"error": "Failed to send OTP", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                return Response({"error": "An unexpected error occurred while sending OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data['otp']

            # Validate OTP
            stored_otp_data = otp_storage.get(phone_number)
            if not stored_otp_data:
                return Response({"error": "OTP not found or expired"}, status=status.HTTP_400_BAD_REQUEST)

            stored_otp, timestamp = stored_otp_data

            # Checking the OTP expiration (valid for 5 minutes)
            current_time = time.time()
            if current_time - timestamp > 300:  # 300 seconds = 5 minutes
                del otp_storage[phone_number]
                return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

            if stored_otp == otp:
                # Checking if the user already exists
                user, created = User.objects.get_or_create(phone_number=phone_number)

                if created:
                    # Creating a new UserProfile for the new user
                    UserProfile.objects.create(user=user, phone_number=phone_number)

                # If user is verified already, return the success message
                if user.is_verified:
                    return Response({"message": "User is already verified and logged in"}, status=status.HTTP_200_OK)

                # Verify the user and save
                user.is_verified = True
                user.save()

                # Log user creation or login
                if created:
                    logger.info(f"New user created with phone number {phone_number}")
                    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
                else:
                    logger.info(f"User logged in with phone number {phone_number}")
                    return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)

            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
