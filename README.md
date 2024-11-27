# Twillio

This project demonstrates how to send OTP (One-Time Password) messages using the Twilio API in a Django Rest Framework (DRF) application. The backend allows you to send OTP via SMS to any verified phone number using Twilio's messaging service.
## Features

- **OTP Generation:** : Generates a unique OTP for each user request
- **Twillio Integration:** Sends OTP via Twilio's SMS API.
- **Verifed Phone Numbers:** Ensures OTP is sent to a phone number that's verified with Twilio.
- **Secure Credential Handling:** Uses environment variables for secure handling of Twilio credentials.


## Prerequisties

- **Twillio Account:** You need a Twilio account to send SMS using their API. You can sign up at Twilio.
- **Twillio Phone Number:** A Twillio phone number to send SMS


## Getting Started

To run the Twillio Project locally, follow these steps:

### 1. Clone the Repository:
   ```bash
   git clone https://github.com/Pooja1030/Twillio.git
   ```
   ```bash
   cd Twillio
   ```
### 2. Create a Virtual Environment:

   For better project management, create a virtual environment to isolate your dependencies.

   Windows:
    ```bash
    python -m venv venv
    ```
   Linux/macOs:
    ```bash
    python3 -m venv venv
    ```

   Activate the virtual environment:
   Windows:
     ```bash
     venv\Scripts\activate
     ```
   Linux/macOs:
     ```bash
     source venv/bin/activate
     ```
    
### 3. Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
### 4. Set Up Twillio Credentials:

   **Create a .env file in the root of the project and add your Twillio credentials:**
  ```bash
  TWILIO_ACCOUNT_SID = 'your_account_sid'
  TWILIO_AUTH_TOKEN = 'your_auth_token'
  TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'
  ```

  Account SID: Found in your Twilio console.
  Auth Token: Available in your Twilio console.
  Twilio Phone Number: Your Twilio SMS-enabled phone number.

### 5. Apply Migrations:
 
   **Since this is a Django project, apply the migrations for the database:**

  ```bash
python manage.py migrations
python manage.py migrate
```

### 6. Run the Application:
    ```bash
    python manage.py runserver
    ```

### 7: Send OTP (Using Postman or any API Client):
  Request Type: POST
  Endpoint: /send-otp/
  Body (JSON format):

```json

{
  "to": "recipient_phone_number"
}
```

**Where:**
otp: The phone number you want to send the OTP to (must be a verified Twilio number).

### 8: Verify OTP (Using Postman or any API Client):
Request Type: POST
Endpoint: /verify-otp/
Body (JSON format):
```json
{
  "otp": "generated_otp"
}
```

**Where:**
otp: The OTP sent to the phone number in the previous request.

### API Endpoints 
### 1. /send-otp/
Method: POST
Description: Sends a generated OTP to the specified phone number.
Request Body:
```json
{
  "to": "recipient_phone_number"
}
```
Response:
```json
{
  "message": "OTP sent successfully."
}
```

### 2. /verify-otp/
Method: POST
Description: Verifies the OTP sent to the phone number.
Request Body:
```json
{
  "otp": "generated_otp"
}
```
Response:
```json

{
  "message": "OTP verified successfully."
}
```

### Troubleshooting
Same "From" and "To" numbers: Ensure the phone number you're sending the OTP to is different from the Twilio number you have. It should be a verified number in your Twilio account.
Blocked Push: If your push is blocked due to secret scanning, remove the Twilio credentials from your Git history and re-commit the changes.

### Example Postman Request for Sending OTP
POST: http://localhost:8000/send-otp/
Body (JSON):
```json
{
  "to": "+1234567890"
}
```
### Example Postman Request for Verifying OTP
POST: http://localhost:8000/verify-otp/
Body (JSON):
```json

{
  "otp": "123456"
}
```


### Technologies Used:
Twilio API: Used for sending OTP via SMS.
Django: Backend web framework for handling requests.
Django Rest Framework (DRF): Used for building the API.
Dotenv: For managing environment variables securely.
Postman: For testing the API.    
