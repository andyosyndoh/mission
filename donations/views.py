
# Create your views here.
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Donation
import uuid
from django.contrib import messages
from django.core.exceptions import ValidationError
import logging


def donation_form(request):
    """Render the donation form"""
    return render(request, 'base.html')
# Set up logging
logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

def process_donation(request):
    """Process the donation form and redirect to Flutterwave"""
    if request.method == 'POST':
        logger.info("Form submitted successfully.")
        try:
            # Extract form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            amount = request.POST.get('amount')
            phone = request.POST.get('phone_number', '')
            payment_method = request.POST.get('payment_method')
            mpesa_message = request.POST.get('mpesa_message', '')  # M-Pesa prompt message
            currency = request.POST.get('currency', 'KES')  # Default to KES, can be changed based on selection
            
            logger.info(f"Form data: name={name}, email={email}, amount={amount}, phone={phone}, payment_method={payment_method}")

            # Generate a unique transaction reference
            tx_ref = f"DON-{uuid.uuid4().hex[:10]}"
            logger.info(f"Transaction reference: {tx_ref}")

            # Create the donation record
            donation = Donation.objects.create(
                amount=amount,
                currency=currency,
                name=name,
                email=email,
                phone_number=phone,
                payment_method=payment_method,
                transaction_ref=tx_ref,
                mpesa_message=mpesa_message if payment_method == 'mpesa' else '',
            )
            logger.info(f"Donation record created: {donation}")

            # Prepare redirect URL for after payment
            redirect_url = request.build_absolute_uri(reverse('payment_callback'))
            logger.info(f"Redirect URL: {redirect_url}")

            # Configure Flutterwave API request
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}'
            }

            payload = {
                'tx_ref': tx_ref,
                'amount': str(amount),
                'currency': currency,
                'redirect_url': redirect_url,
                'customer': {
                    'email': email,
                    'name': name,
                    'phone_number': phone
                },
                'meta': {
                    'donation_id': str(donation.id)
                },
                'customizations': {
                    'title': 'Hospital Donation',
                    'description': 'Donation to support our hospital',
                    'logo': request.build_absolute_uri('/static/images/hospital-logo.png')
                }
            }

            # For M-Pesa integration
            if payment_method == 'mpesa':
                if not phone:
                    messages.error(request, 'Phone number is required for M-Pesa payments.')
                    logger.error("Phone number is missing for M-Pesa payment.")
                    return redirect('donation_form')
                payload['payment_options'] = 'mpesa'
                payload['mobile_money'] = {
                    'phone': phone,
                    'network': 'mpesa',
                    'voucher': mpesa_message  # This will appear in M-Pesa prompt
                }
                logger.info(f"M-Pesa payload: {payload['mobile_money']}")

            # Make API request to Flutterwave
            logger.info("Making API request to Flutterwave...")
            response = requests.post(
                'https://api.flutterwave.com/v3/payments',
                headers=headers,
                json=payload
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            response_data = response.json()
            logger.info(f"Flutterwave API response: {response_data}")

            if response_data.get('status') == 'success':
                # Redirect to Flutterwave payment page
                logger.info("Payment initialization successful. Redirecting to Flutterwave payment page.")
                return redirect(response_data['data']['link'])
            else:
                # Handle error
                donation.payment_status = 'failed'
                donation.save()
                messages.error(request, 'Payment initialization failed. Please try again.')
                logger.error(f"Payment initialization failed. Response: {response_data}")
                return redirect('donation_form')

        except requests.exceptions.RequestException as e:
            # Handle API request errors
            logger.error(f"Flutterwave API request failed: {e}")
            donation.payment_status = 'failed'
            donation.save()
            messages.error(request, f'An error occurred while processing your payment: {str(e)}')
            return redirect('donation_form')

        except Exception as e:
            # Handle unexpected errors
            logger.error(f"An unexpected error occurred: {e}")
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('donation_form')

    # If the request method is not POST, redirect to the donation form
    return redirect('donation_form')

@csrf_exempt
@require_POST
def webhook(request):
    """Handle Flutterwave webhook notifications"""
    # Verify the webhook signature
    signature = request.headers.get('verifi-hash')
    if not signature or signature != settings.FLUTTERWAVE_SECRET_HASH:
        return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=401)
    
    # Parse webhook data
    try:
        payload = json.loads(request.body)
        if payload.get('event') == 'charge.completed':
            data = payload.get('data', {})
            tx_ref = data.get('tx_ref')
            status = data.get('status')
            
            # Find the donation
            try:
                donation = Donation.objects.get(transaction_ref=tx_ref)
                
                # Update donation status
                if status == 'successful':
                    donation.payment_status = 'successful'
                    donation.transaction_id = data.get('id')
                else:
                    donation.payment_status = 'failed'
                    
                donation.save()
                
                return JsonResponse({'status': 'success'})
                
            except Donation.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Donation not found'}, status=404)
        
        return JsonResponse({'status': 'success'})
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

@csrf_exempt
@csrf_exempt
def payment_callback(request):
    """Handle payment callback from Flutterwave"""
    status = request.GET.get('status')
    tx_ref = request.GET.get('tx_ref')
    transaction_id = request.GET.get('transaction_id')
    
    logger.info(f"Payment callback received - Status: {status}, TX_REF: {tx_ref}, Transaction ID: {transaction_id}")

    if status and tx_ref:
        try:
            donation = Donation.objects.get(transaction_ref=tx_ref)
            logger.info(f"Donation found: {donation}")

            # Verify payment with Flutterwave API
            if status == 'successful' and transaction_id:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}'
                }
                
                verify_url = f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify'
                logger.info(f"Verifying payment with Flutterwave API: {verify_url}")

                try:
                    response = requests.get(verify_url, headers=headers)
                    data = response.json()
                    logger.info(f"Flutterwave verification response: {data}")

                    if (response.status_code == 200 and 
                        data.get('status') == 'success' and 
                        data.get('data', {}).get('status') == 'successful' and
                        data.get('data', {}).get('amount') >= float(donation.amount)):
                        
                        donation.payment_status = 'successful'
                        donation.transaction_id = transaction_id
                        donation.save()
                        logger.info("Payment verification successful. Redirecting to success page.")
                        
                        messages.success(request, 'Thank you for your donation!')
                        return redirect('donation_success')
                    else:
                        donation.payment_status = 'failed'
                        donation.save()
                        logger.error("Payment verification failed. Redirecting to failed page.")
                        
                        messages.error(request, 'Payment verification failed. Please contact support.')
                        return redirect('donation_failed')
                        
                except Exception as e:
                    donation.payment_status = 'failed'
                    donation.save()
                    logger.error(f"Payment verification error: {e}")
                    
                    messages.error(request, f'Payment verification error: {str(e)}')
                    return redirect('donation_failed')
            else:
                donation.payment_status = 'failed'
                donation.save()
                logger.error("Payment was not successful. Redirecting to failed page.")
                
                messages.error(request, 'Payment was not successful.')
                return redirect('donation_failed')
                
        except Donation.DoesNotExist:
            logger.error("Donation reference not found. Redirecting to failed page.")
            
            messages.error(request, 'Donation reference not found.')
            return redirect('donation_failed')
    
    logger.error("Invalid payment callback. Redirecting to failed page.")
    
    messages.error(request, 'Invalid payment callback')
    return redirect('donation_failed')

# def donation_success(request):
#     """Render success page after donation"""
#     return render(request, 'donations/success.html')

# def donation_failed(request):
#     """Render failure page after donation"""
#     return render(request, 'donations/failed.html')

def validate_amount(amount):
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValidationError("Amount must be greater than 0.")
    except ValueError:
        raise ValidationError("Invalid amount.")


def donation_success(request):
    """Render success page after donation"""
    # Retrieve the latest donation for the current user (if applicable)
    donation = Donation.objects.filter(email=request.user.email).last() if request.user.is_authenticated else None
    return render(request, 'donations/success.html', {'donation': donation})

def donation_failed(request):
    """Render failure page after donation"""
    return render(request, 'donations/failed.html')