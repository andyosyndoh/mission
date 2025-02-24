from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from .forms import AppointmentForm
from .models import Doctor
import requests
# import stripe
# import datetime
from .mpesa_api import stk_push


def initiate_payment(request):
    phone_number = request.GET.get("phone")
    amount = request.GET.get("amount")

    if not phone_number or not amount:
        return JsonResponse({"error": "Phone number and amount are required"}, status=400)

    response = stk_push(phone_number, int(amount))

    return JsonResponse(response)

def donation_view(request):
    if request.method == 'POST':
        # Process the donation form here
        # e.g. read form data, save to DB, redirect or render success page
        # ...
        return redirect('home')  # or wherever you want to go after submission
    else:
        # If someone visits /donation/ via GET, just show a simple page or redirect
        return render(request, 'some_template.html')
    
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
