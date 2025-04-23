from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import BaseAppointmentForm, NewsletterForm, ContactForm
from .models import TeamMember, Subscriber, Testimonial
from django.urls import reverse
import logging
logger = logging.getLogger(__name__)

def book_appointment(request):
    if request.method == "POST":
        form = BaseAppointmentForm(request.POST)

        if form.is_valid():
            # Save to database first
            appointment = form.save(commit=False)
            appointment.save()

            # Prepare email
            subject = f"New Appointment Request from {appointment.full_name}"
            body_lines = [
                f"Full Name: {appointment.full_name}",
                f"Email: {appointment.email}",
                f"Date: {appointment.date}",
                f"Time: {appointment.time}",
            ]
            
            if appointment.department:
                body_lines.insert(2, f"Department: {appointment.department}")
            if appointment.phone:
                body_lines.insert(4, f"Phone: {appointment.phone}")
            if appointment.message:
                body_lines.append(f"Message: {appointment.message}")            

            try:
                send_mail(
                    subject,
                    '\n'.join(body_lines),
                    "hmissionhospital@gmail.com",  # sender email
                    ["hmissionhospital@gmail.com"],  # receiving email
                    fail_silently=False,
                )
                messages.success(request, "Your appointment has been booked successfully! We'll get back to you for confirmation.")
            except Exception as e:
                logger.error(f"Email failed:  {str(e)}")
                messages.error(request, "Something went wrong. Please try again.")
                
            return redirect("home")  # Redirect to the appointment page or any success page

    else:
        form = BaseAppointmentForm()

    return render(request, "home.html", {"form": form})

def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            if Subscriber.objects.filter(email=subscriber.email).exists():
                messages.info(request, "You're already subscribed!")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            subscriber.save()
            
            # Send confirmation email
            confirmation_link = request.build_absolute_uri(
                reverse('confirm_subscription', args=[subscriber.confirmation_token])
            )
            
            send_mail(
                'Confirm your subscription',
                f'Click to confirm: {confirmation_link}',
                'noreply@yourhospital.com',
                [subscriber.email],
                fail_silently=False,
            )
            
            messages.success(request, "Confirmation email sent! Please check your inbox.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        messages.error(request, "Invalid email address")
    return redirect('home')

def confirm_subscription(request, token):
    try:
        subscriber = Subscriber.objects.get(confirmation_token=token)
        if not subscriber.confirmed:
            subscriber.confirmed = True
            subscriber.save()
            messages.success(request, "Subscription confirmed!")
        else:
            messages.info(request, "Subscription already confirmed")
    except Subscriber.DoesNotExist:
        messages.error(request, "Invalid confirmation link")
    
    return redirect('home')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)

             # Prepare email content
            subject = f"New Contact Message from {contact.name}"
            body_lines = [
                f"Name: {contact.name}",
                f"Email: {contact.email}",
                f"Subject: {contact.subject}",
                f"Message: {contact.message}",
            ]

            try:
                send_mail(
                    subject,
                    '\n'.join(body_lines),
                    "hmissionhospital@gmail.com",  # Sender email
                    ["hmissionhospital@gmail.com"],  # Where hospital reads messages
                    fail_silently=False,
                )
                contact.save()
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                logger.error(f"Contact form email failed: {str(e)}")
                messages.error(request, "Something went wrong. Please try again.")
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

# Create your views here.
def home(request):
    featured_members = TeamMember.objects.filter(is_featured=True)[:4]
    testimonials = Testimonial.objects.filter(active=True)
    context = {
        'featured_members': featured_members,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)

def about(request):
    testimonials = Testimonial.objects.filter(active=True)
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'about.html', context)

def services(request):
    return render(request, 'services.html', {})

def team(request):
    team_members = TeamMember.objects.all().order_by('member_type', 'name')
    return render(request, 'doctors.html', {'team_members': team_members})

def contact(request):
    return render(request, 'contact.html', {})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)