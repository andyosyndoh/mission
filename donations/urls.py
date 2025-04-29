# donations/urls.py
from django.urls import path
from . import views

app_name = 'donations'  # Namespace declaration

urlpatterns = [
    path('initiate/', views.initiate_donation, name='initiate_donation'),
    path('callback/', views.payment_callback, name='payment_callback'),
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
    path('ipn/', views.ipn_handler, name='ipn_handler'),
]