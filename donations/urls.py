from django.urls import path
from . import views
from .views import initiate_donation


app_name = 'donations'

urlpatterns = [
    path('initiate/', views.initiate_donation, name='initiate_donation'),
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
    path('callback/', views.payment_callback, name='payment_callback'),
    path('ipn/', views.ipn_handler, name='ipn_handler'),
]
