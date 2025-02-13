from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import AppointmentForm

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

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

def services(request):
    return render(request, 'services.html', {})

def doctors(request):
    return render(request, 'doctors.html', {})

def contact(request):
    return render(request, 'contact.html', {})
