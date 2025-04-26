from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import PesapalTransaction
from .pesapal_client import PesapalV3
from django.conf import settings
import uuid
import json
import re

def format_phone_number(phone):
    """Convert 07... or 7... to 2547... format"""
    phone = str(phone).strip().replace(" ", "")
    if phone.startswith("0") and len(phone) == 10:
        return "254" + phone[1:]
    elif phone.startswith("7") and len(phone) == 9:
        return "254" + phone
    return phone  # Assume already formatted if not matching

@csrf_exempt
def initiate_pesapal(request):
    if request.method == 'POST':
        try:
            # Validate required fields
            amount = request.POST.get('amount')
            mpesa_number = request.POST.get('mpesa_number')
            
            if not amount or not mpesa_number:
                raise ValueError("Amount and M-Pesa number are required")

            # Create donation transaction record
            transaction = PesapalTransaction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                amount=amount,
                currency=request.POST.get('currency', 'KES'),
                donation_purpose=request.POST.get('purpose', 'General Donation'),
                phone_number=mpesa_number  # Store original number
            )
            
            # Initialize Pesapal client
            pesapal = PesapalV3()
            auth_token = pesapal.get_auth_token()
            ipn_id = pesapal.register_ipn(auth_token)
            
            # Format phone number for Pesapal
            formatted_phone = format_phone_number(mpesa_number)
            
            # Prepare donation payload
            order_data = {
                "id": str(transaction.order_id),
                "currency": transaction.currency,
                "amount": float(amount),
                "description": f"{settings.PESAPAL_DONATION_DESCRIPTION} - {transaction.donation_purpose}",
                "callback_url": settings.PESAPAL_CALLBACK_URL,
                "notification_id": ipn_id,
                "billing_address": {
                    "email_address": request.POST.get('email', ''),
                    "phone_number": formatted_phone,  # Use formatted number
                    "first_name": request.POST.get('first_name', ''),
                    "last_name": request.POST.get('last_name', ''),
                }
            }
            
            # Submit to Pesapal
            response = pesapal.create_order(auth_token, order_data)
            
            if not response or 'redirect_url' not in response:
                raise ValueError("Failed to get payment URL from Pesapal")
            
            transaction.pesapal_id = response.get('order_tracking_id')
            transaction.save()
            
            return redirect(response['redirect_url'])
            
        except Exception as e:
            return render(request, 'pesapal/error.html', {
                'error': f"Payment initialization failed: {str(e)}"
            })
    
    return redirect('home')

@csrf_exempt
def pesapal_callback(request):
    tracking_id = request.GET.get('OrderTrackingId')
    try:
        transaction = PesapalTransaction.objects.get(pesapal_id=tracking_id)
        transaction.status = request.GET.get('PaymentStatus', 'PENDING')
        transaction.save()
        return render(request, 'pesapal/status.html', {
            'transaction': transaction,
            'donation_purpose': transaction.donation_purpose
        })
    except PesapalTransaction.DoesNotExist:
        return render(request, 'pesapal/error.html', {'error': 'Invalid transaction'})

@csrf_exempt
def pesapal_ipn(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            transaction = PesapalTransaction.objects.get(
                pesapal_id=data.get('OrderNotificationId')
            )
            transaction.status = data.get('Status', 'PENDING')
            transaction.save()
            return HttpResponse(status=200)
        except (PesapalTransaction.DoesNotExist, KeyError, json.JSONDecodeError) as e:
            return HttpResponse(status=400)
    return HttpResponse(status=405)