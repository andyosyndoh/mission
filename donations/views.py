import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from .models import Donation
from .services import PesapalGateway

logger = logging.getLogger(__name__)

@transaction.atomic
def initiate_donation(request):
    """Handle donation form submission"""
    if request.method == 'POST':
        try:
            # Create donation record
            donation = Donation.objects.create(
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                amount=request.POST.get('amount'),
                currency=request.POST.get('currency'),
                mpesa_number=request.POST.get('mpesa_number', '')
            )

            # Prepare Pesapal order data
            pesapal = PesapalGateway()
            order_data = {
                'reference': donation.id,
                'amount': donation.amount,
                'currency': donation.currency,
                'description': f"Donation from {donation.full_name}",
                'email': donation.email,
                'phone': donation.mpesa_number if donation.currency == 'KES' else donation.phone,
                'country_code': 'KE' if donation.currency == 'KES' else 'US',
                'first_name': donation.full_name.split()[0],
                'last_name': ' '.join(donation.full_name.split()[1:]) if len(donation.full_name.split()) > 1 else '',
            }

            # Get Pesapal redirect URL
            redirect_url = pesapal.create_order(order_data)
            if not redirect_url:
                logger.error("Pesapal did not return a redirect_url.")
                return redirect("donation_failed")
            
            return redirect(redirect_url)

        except Exception as e:
            logger.error(f"Donation initiation failed: {str(e)}", exc_info=True)
            messages.error(request, "Payment initialization failed. Please try again.")
            return redirect('donations:payment_failed')

    messages.warning(request, "Invalid request method")
    return redirect('home')

@csrf_exempt
def payment_callback(request):
    """Handle Pesapal callback redirect"""
    try:
        tracking_id = request.GET.get('OrderTrackingId')
        merchant_reference = request.GET.get('OrderMerchantReference')

        if not tracking_id or not merchant_reference:
            logger.error("Missing tracking ID or merchant reference in callback")
            return redirect('donations:payment_failed')

        # Retrieve donation using your internal reference (merchant_reference)
        donation = Donation.objects.get(id=merchant_reference)
        donation.pesapal_tracking_id = tracking_id
        donation.status = 'pending_verification'
        donation.save()

        messages.info(request, "Payment received. Processing confirmation...")
        return redirect('donations:payment_success')

    except Donation.DoesNotExist:
        logger.error(f"Donation not found for reference: {merchant_reference}")
        messages.error(request, "Invalid transaction reference")
        return redirect('donations:payment_failed')


@csrf_exempt
def ipn_handler(request):
    """Handle Instant Payment Notification (IPN)"""
    if request.method == 'POST':
        try:
            content_type = request.META.get('CONTENT_TYPE', '')
            raw_body = request.body.decode('utf-8')
            logger.info(f"Content-Type: {content_type}")
            logger.info(f"Raw IPN body: {raw_body}")

            # Parse JSON or form data depending on Pesapal's content type
            if 'application/json' in content_type:
                ipn_data = json.loads(raw_body)
            elif 'application/x-www-form-urlencoded' in content_type:
                ipn_data = request.POST
            else:
                logger.error("Unsupported content type")
                return JsonResponse({'error': 'Unsupported content type'}, status=400)

            # Extract data
            tracking_id = ipn_data.get('OrderMerchantReference')
            transaction_id = ipn_data.get('TransactionId')
            status = ipn_data.get('OrderStatus', '').lower()

            if not all([tracking_id, transaction_id, status]):
                logger.error("Missing parameters in IPN")
                return JsonResponse({'error': 'Missing parameters'}, status=400)

            # Update donation
            donation = Donation.objects.get(id=tracking_id)
            donation.pesapal_tracking_id = transaction_id
            donation.status = status
            donation.save()

            return JsonResponse({'status': 'success'}, status=200)

        except json.JSONDecodeError:
            logger.error("Invalid JSON in IPN")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Donation.DoesNotExist:
            logger.error(f"IPN: Donation not found - {tracking_id}")
            return JsonResponse({'error': 'Donation not found'}, status=404)
        except Exception as e:
            logger.error(f"IPN handling failed: {str(e)}", exc_info=True)
            return JsonResponse({'error': 'Server error'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def payment_success(request):
    """Display success page"""
    return render(request, 'donations/success.html')

def payment_failed(request):
    """Display failure page"""
    return render(request, 'donations/failed.html')