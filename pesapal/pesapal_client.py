import requests
from requests_oauthlib import OAuth1
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class PesapalV3:
    def __init__(self):
        self.base_url = "https://cybqa.pesapal.com/pesapalv3" if settings.PESAPAL_ENVIRONMENT == 'sandbox' else "https://pay.pesapal.com/v3"
        self.oauth = OAuth1(
            settings.PESAPAL_CONSUMER_KEY,
            settings.PESAPAL_CONSUMER_SECRET,
            signature_type='auth_header'
        )
    
    def get_auth_token(self):
        try:
            response = requests.post(
                f"{self.base_url}/api/Auth/RequestToken",
                auth=self.oauth
            )
            response.raise_for_status()
            return response.json().get('token')
        except Exception as e:
            logger.error(f"Auth Error: {str(e)}")
            return None
    
    def register_ipn(self, token):
        try:
            response = requests.post(
                f"{self.base_url}/api/URLSetup/RegisterIPN",
                json={
                    "url": settings.PESAPAL_IPN_URL,
                    "ipn_notification_type": "POST"
                },
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status()
            return response.json().get('ipn_id')
        except Exception as e:
            logger.error(f"IPN Registration Error: {str(e)}")
            return None
    
    def create_order(self, token, order_data):
        try:
            response = requests.post(
                f"{self.base_url}/api/Transactions/SubmitOrderRequest",
                json=order_data,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Order Creation Error: {str(e)}")
            return None