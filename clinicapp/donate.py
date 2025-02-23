# models.py
from django.db import models
from django.utils import timezone

class Donation(models.Model):
    PAYMENT_METHODS = (
        ('BANK', 'Bank Transfer'),
        ('MPESA', 'M-Pesa'),
    )
    
    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')  # KES for Kenyan Shilling
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    donor_name = models.CharField(max_length=100)
    # donor_email = models.EmailField()
    donor_country = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.donor_name} - {self.amount} {self.currency}"

# views.py
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .models import Donation
from datetime import datetime
# import requests
from django.views.decorators.csrf import csrf_exempt

def donation_page(request):
    return render(request, 'donations/donate.html')

@csrf_exempt
def process_mpesa_donation(request):
    if request.method == 'POST':
        # Initialize M-Pesa payment
        # This is a simplified version - you'll need to implement the actual M-Pesa API
        amount = request.POST.get('amount')
        phone_number = request.POST.get('phone_number')
        
        donation = Donation.objects.create(
            amount=amount,
            payment_method='MPESA',
            donor_name=request.POST.get('name'),
            donor_email=request.POST.get('email'),
            donor_country='Kenya'  # Default for M-Pesa
        )
        
        # Here you would integrate with M-Pesa API
        # Example M-Pesa integration code would go here
        
        return JsonResponse({'status': 'success', 'message': 'M-Pesa payment initiated'})

def process_bank_donation(request):
    if request.method == 'POST':
        # Create donation record
        donation = Donation.objects.create(
            amount=request.POST.get('amount'),
            currency=request.POST.get('currency'),
            payment_method='BANK',
            donor_name=request.POST.get('name'),
            donor_email=request.POST.get('email'),
            donor_country=request.POST.get('country')
        )
        
        # Return bank account details
        return JsonResponse({
            'status': 'success',
            'bank_details': {
                'bank_name': settings.HOSPITAL_BANK_NAME,
                'account_name': settings.HOSPITAL_ACCOUNT_NAME,
                'account_number': settings.HOSPITAL_ACCOUNT_NUMBER,
                'swift_code': settings.HOSPITAL_SWIFT_CODE,
                'reference': f'DON{donation.id}'  # Unique reference for tracking
            }
        })

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('donate/', views.donation_page, name='donation_page'),
    path('donate/mpesa/', views.process_mpesa_donation, name='mpesa_donation'),
    path('donate/bank/', views.process_bank_donation, name='bank_donation'),
]