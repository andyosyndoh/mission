import requests
import logging
import json  # <-- Added for logging payloads
from django.conf import settings
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class PesapalGateway:
    def __init__(self):
        self.base_url = (
            "https://cybqa.pesapal.com/pesapalv3"
            if settings.PESAPAL_ENVIRONMENT == "sandbox" 
            else "https://pay.pesapal.com/v3"
        )
        self.token = None
    
    def _authenticate(self):
        """Get OAuth 2.0 Bearer Token"""
        auth_url = f"{self.base_url}/api/Auth/RequestToken"

        payload = {
            "consumer_key": settings.PESAPAL_CONSUMER_KEY,
            "consumer_secret": settings.PESAPAL_CONSUMER_SECRET
        }
        
        try:
            response = requests.post(auth_url, json=payload, headers={
                "Content-Type": "application/json"
            })
            logger.debug(f"Authentication response: {response.text}")
            response.raise_for_status()
            self.token = response.json().get("token")
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise

    def create_order(self, order_data):
        """Create Pesapal payment order"""
        self._authenticate()
        order_url = f"{self.base_url}/api/Transactions/SubmitOrderRequest"

        payload = {
            "id": str(order_data['reference']),
            "currency": order_data['currency'],
            "amount": str(order_data['amount']),
            "description": order_data['description'],
            "callback_url": settings.PESAPAL_CALLBACK_URL,
            "notification_id": settings.PESAPAL_IPN_ID,
            "billing_address": {
                "email_address": order_data['email'],
                "phone_number": order_data['phone'],
                "country_code": order_data['country_code'],
                "first_name": order_data['first_name'],
                "last_name": order_data['last_name']
            }
        }

        logger.debug(f"Order payload: {json.dumps(payload, indent=2)}")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            response = requests.post(order_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json().get("redirect_url")
        except requests.exceptions.RequestException as e:
            logger.error(f"Order creation failed: {str(e)}")
            raise

    def check_payment_status(self, order_id):
        """Verify payment status directly from Pesapal"""
        self._authenticate()
        status_url = urljoin(self.base_url, f"/api/Transactions/GetTransactionStatus?orderTrackingId={order_id}")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(status_url, headers=headers)
            response.raise_for_status()
            return response.json().get('payment_status', 'pending').lower()
        except Exception as e:
            logger.error(f"Status check failed: {str(e)}")
            return 'pending'
