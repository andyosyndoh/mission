from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import AppointmentForm, NewsletterForm
from .models import TeamMember, Subscriber, Testimonial
from django.urls import reverse

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
    return render(request, 'about.html', {})

def services(request):
    return render(request, 'services.html', {})

def team(request):
    team_members = TeamMember.objects.all().order_by('member_type', 'name')
    return render(request, 'doctors.html', {'team_members': team_members})

def contact(request):
    return render(request, 'contact.html', {})
