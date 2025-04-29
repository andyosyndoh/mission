import requests
from django.conf import settings

class PesapalGateway:
    def __init__(self):
        self.base_url = "https://cybqa.pesapal.com/pesapalv3" if settings.PESAPAL_ENVIRONMENT == "sandbox" \
            else "https://pay.pesapal.com/v3"
        self.token = None
    
    def _authenticate(self):
        auth_url = f"{self.base_url}/api/Auth/RequestToken"
        payload = {
            "consumer_key": settings.PESAPAL_CONSUMER_KEY,
            "consumer_secret": settings.PESAPAL_CONSUMER_SECRET
        }
        response = requests.post(auth_url, json=payload)
        self.token = response.json().get("token")
    
    def create_order(self, order_data):
        self._authenticate()
        order_url = f"{self.base_url}/api/Transactions/SubmitOrderRequest"
        
        payload = {
            "id": order_data['reference'],
            "currency": order_data['currency'],
            "amount": float(order_data['amount']),
            "description": order_data['description'],
            "callback_url": order_data.get('callback_url', ''),
            "notification_id": settings.PESAPAL_IPN_ID,
            "billing_address": {
                "email_address": order_data['email'],
                "phone_number": order_data['phone_number'],
                "country_code": order_data['billing_address']['country_code'],
                "first_name": order_data['billing_address']['first_name'],
                "last_name": order_data['billing_address']['last_name']
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(order_url, json=payload, headers=headers)
        return response.json().get("redirect_url")