from django.urls import path
from . import views

app_name = 'pesapal'

urlpatterns = [
    path('initiate/', views.initiate_pesapal, name='initiate'),
    path('callback/', views.pesapal_callback, name='callback'),
    path('ipn/', views.pesapal_ipn, name='ipn'),
]