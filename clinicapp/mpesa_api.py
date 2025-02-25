import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
import requests
import base64
import datetime


# Get M-Pesa Access Token
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Failed to get access token:", response.json())
        return None
    
def stk_push(phone_number, amount):
    access_token = get_access_token()
    if access_token is None:
        return {"error": "Failed to generate access token"}

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode()).decode()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "KoruHealth",
        "TransactionDesc": "Payment for services",
    }

    response = requests.post(url, json=payload, headers=headers)

    try:
        return response.json()  # Ensure it returns a valid JSON response
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON response from M-Pesa"}
