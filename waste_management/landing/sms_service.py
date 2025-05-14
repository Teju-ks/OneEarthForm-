from twilio.rest import Client

# Twilio credentials (replace with your actual credentials)
TWILIO_ACCOUNT_SID = ' ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# This is a placeholder value. Replace with your actual Twilio Account SID.'
TWILIO_AUTH_TOKEN = '   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# This is a placeholder value. Replace with your actual Twilio Auth Token.'
TWILIO_PHONE_NUMBER = '+    XXXXXXXXXX'
# This is a placeholder value. Replace with your actual Twilio phone number.'

def send_sms(to_phone_number, message):
    """
    Sends an SMS to the specified phone number using Twilio.
    
    :param to_phone_number: The recipient's phone number (e.g., '+1234567890').
    :param message: The message to send.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone_number  # Use the dynamic phone number
        )
        print(f"SMS sent successfully: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")