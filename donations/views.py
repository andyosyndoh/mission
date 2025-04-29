# donations/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.db import transaction
import logging
from .models import Donation
from .services import PesapalGateway

logger = logging.getLogger(__name__)

@transaction.atomic
def initiate_donation(request):
    """Handle donation form submission and initiate Pesapal payment"""
    if request.method == 'POST':
        try:
            # Create donation record
            donation = Donation.objects.create(
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                amount=request.POST.get('amount'),
                currency=request.POST.get('currency'),
                purpose=request.POST.get('purpose'),
                mpesa_number=request.POST.get('mpesa_number', '')
            )

            # Initialize Pesapal gateway
            pesapal = PesapalGateway()
            callback_url = request.build_absolute_uri(reverse('donations:payment_callback'))

            # Prepare order data
            order_data = {
                'amount': donation.amount,
                'currency': donation.currency,
                'description': f"Donation for {donation.purpose}",
                'reference': str(donation.id),
                'email': donation.email,
                'phone_number': donation.mpesa_number if donation.currency == 'KES' else donation.phone,
                'callback_url': callback_url,
                'billing_address': {
                    'first_name': donation.full_name.split()[0],
                    'last_name': ' '.join(donation.full_name.split()[1:]) if len(donation.full_name.split()) > 1 else '',
                    'country_code': 'KE' if donation.currency == 'KES' else 'US'
                }
            }

            # Get Pesapal payment URL
            redirect_url = pesapal.create_order(order_data)
            if not redirect_url:
                messages.error(request, "Failed to initialize payment gateway")
                return redirect('donations:payment_failed')

            return redirect(redirect_url)

        except Exception as e:
            logger.error(f"Donation initiation failed: {str(e)}", exc_info=True)
            messages.error(request, f"Payment initialization failed: {str(e)}")
            return redirect('donations:payment_failed')

    messages.warning(request, "Invalid request method")
    return redirect('home')

@csrf_exempt
def payment_callback(request):
    """Handle Pesapal payment callback"""
    try:
        merchant_reference = request.GET.get('OrderTrackingId')
        if not merchant_reference:
            logger.error("Missing OrderTrackingId in callback")
            return redirect('donations:payment_failed')

        donation = Donation.objects.get(id=merchant_reference)
        donation.pesapal_transaction_id = request.GET.get('OrderMerchantReference', '')
        
        # Update status based on Pesapal response
        status = request.GET.get('status', 'pending').lower()
        donation.status = 'completed' if status == 'completed' else 'failed'
        donation.save()

        if donation.status == 'completed':
            messages.success(request, "Payment completed successfully!")
            return redirect('donations:payment_success')
        else:
            messages.warning(request, "Payment processing not completed")
            return redirect('donations:payment_failed')

    except Donation.DoesNotExist:
        logger.error(f"Donation not found for reference: {merchant_reference}")
        messages.error(request, "Invalid transaction reference")
        return redirect('donations:payment_failed')
    except Exception as e:
        logger.error(f"Callback handling failed: {str(e)}", exc_info=True)
        messages.error(request, "Payment verification failed")
        return redirect('donations:payment_failed')

@csrf_exempt
def ipn_handler(request):
    """Handle Instant Payment Notification (IPN) from Pesapal"""
    if request.method == 'POST':
        try:
            ipn_data = request.POST.dict()
            logger.info(f"Received IPN: {ipn_data}")

            merchant_reference = ipn_data.get('OrderNotificationMerchantReference')
            transaction_id = ipn_data.get('TransactionId')
            status = ipn_data.get('OrderStatus', '').lower()

            if not all([merchant_reference, transaction_id, status]):
                logger.error("Invalid IPN data received")
                return HttpResponseBadRequest("Invalid IPN data")

            donation = Donation.objects.get(id=merchant_reference)
            donation.pesapal_transaction_id = transaction_id
            donation.status = status
            donation.save()

            logger.info(f"Updated donation {donation.id} status to {status}")
            return HttpResponse(status=200)

        except Donation.DoesNotExist:
            logger.error(f"IPN: Donation not found - {merchant_reference}")
            return HttpResponse(status=404)
        except Exception as e:
            logger.error(f"IPN handling failed: {str(e)}", exc_info=True)
            return HttpResponse(status=500)

    return HttpResponse(status=405)

def payment_success(request):
    """Display payment success page"""
    return render(request, 'donations/payment_success.html')

def payment_failed(request):
    """Display payment failed page"""
    return render(request, 'donations/payment_failed.html')

def donation_list(request):
    """View all donations (protect this in production)"""
    donations = Donation.objects.all().order_by('-created_at')
    return render(request, 'donations/list.html', {'donations': donations})