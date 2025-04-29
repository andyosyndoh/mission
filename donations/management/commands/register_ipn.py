# donations/management/commands/register_ipn.py
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import json

class Command(BaseCommand):
    help = 'Register IPN URL with Pesapal'

    def handle(self, *args, **options):
        try:
            # Authenticate
            auth_url = (
                'https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken' 
                if settings.PESAPAL_ENVIRONMENT == 'sandbox' 
                else 'https://pay.pesapal.com/v3/api/Auth/RequestToken'
            )
            
            auth_data = {
                "consumer_key": settings.PESAPAL_CONSUMER_KEY,
                "consumer_secret": settings.PESAPAL_CONSUMER_SECRET
            }
            
            auth_res = requests.post(auth_url, json=auth_data)
            auth_res.raise_for_status()
            token = auth_res.json().get('token')

            # Register IPN
            ipn_url = (
                'https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN' 
                if settings.PESAPAL_ENVIRONMENT == 'sandbox' 
                else 'https://pay.pesapal.com/v3/api/URLSetup/RegisterIPN'
            )
            
            payload = {
                "url": settings.PESAPAL_IPN_URL,
                "ipn_notification_type": "POST"
            }
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(ipn_url, json=payload, headers=headers)
            response.raise_for_status()
            
            ipn_data = response.json()
            self.stdout.write(self.style.SUCCESS(f'Successfully registered IPN!'))
            self.stdout.write(f'PESAPAL_IPN_ID={ipn_data["ipn_id"]}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'IPN registration failed: {str(e)}'))