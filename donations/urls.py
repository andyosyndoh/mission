from django.urls import path
from . import views

urlpatterns = [
    path('donate/', views.donation_form, name='donation_form'),
    path('process-donation/', views.process_donation, name='process_donation'),
    path('webhook/', views.webhook, name='flutterwave_webhook'),
    path('callback/', views.payment_callback, name='payment_callback'),
    path('success/', views.donation_success, name='donation_success'),
    path('failed/', views.donation_failed, name='donation_failed'),
]
