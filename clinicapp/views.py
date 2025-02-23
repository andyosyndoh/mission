from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from .forms import AppointmentForm
from .models import Doctor, Donation

# Existing Views
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Save to database first
            appointment = form.save()

            # Prepare email
            subject = f"New Appointment Request from {appointment.full_name}"
            body = (
                f"Full Name: {appointment.full_name}\n"
                f"Email: {appointment.email}\n"
                f"Date: {appointment.date}\n"
                f"Time: {appointment.time}\n"
                f"Message: {appointment.message}"
            )            

            try:
                send_mail(
                    subject,
                    body,
                    "noreply@korumissionhospital.com",  # Replace with your sender email
                    ["adakennedy6@gmail.com"],  # Replace with hospital's receiving email
                    fail_silently=False,
                )
                messages.success(request, "Appointment booked and email sent!")
            except Exception as e:
                messages.warning(request, f"Appointment saved but email failed: {str(e)}")
                
            return redirect("home")  # Redirect to the appointment page or any success page

    else:
        form = AppointmentForm()

    return render(request, "home.html", {"form": form})

def home(request):
    featured_doctors = Doctor.objects.filter(is_featured=True)[:4]
    context = {
        'featured_doctors': featured_doctors,
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html', {})

def services(request):
    return render(request, 'services.html', {})

def doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors.html', {'doctors': doctors})

def contact(request):
    return render(request, 'contact.html', {})

# Donation App Views
# def donation_page(request):
#     return render(request, 'donations/donate.html')

# @csrf_exempt
# def process_mpesa_donation(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             donation = Donation.objects.create(
#                 amount=data.get('amount'),
#                 payment_method='MPESA',
#                 donor_name=data.get('name'),
#                 donor_email=data.get('email', ''),
#                 donor_country='Kenya'
#             )
#             # Simulate M-Pesa API call
#             return JsonResponse({'status': 'success', 'message': 'M-Pesa payment initiated'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# @csrf_exempt
# def process_bank_donation(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             donation = Donation.objects.create(
#                 amount=data.get('amount'),
#                 currency=data.get('currency'),
#                 payment_method='BANK',
#                 donor_name=data.get('name'),
#                 donor_email=data.get('email'),
#                 donor_country=data.get('country')
#             )
#             # Send email with bank details
#             send_mail(
#                 'Your Donation Bank Details',
#                 f'Here are the bank details for your donation:\n\n'
#                 f'Bank Name: {settings.HOSPITAL_BANK_NAME}\n'
#                 f'Account Name: {settings.HOSPITAL_ACCOUNT_NAME}\n'
#                 f'Account Number: {settings.HOSPITAL_ACCOUNT_NUMBER}\n'
#                 f'Swift Code: {settings.HOSPITAL_SWIFT_CODE}\n'
#                 f'Reference: DON{donation.id}',
#                 settings.DEFAULT_FROM_EMAIL,
#                 [data.get('email')],
#                 fail_silently=False,
#             )
#             return JsonResponse({'status': 'success'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)