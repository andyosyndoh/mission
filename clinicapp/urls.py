from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('services', views.services, name="services"),
    path('doctors', views.doctors, name="doctors"),
    path('contact', views.contact, name="contact"),
    path('appointment/', views.book_appointment, name="appointment"),
    path('donate/', views.donation_page, name="donation_page"),
    path('donate/mpesa/', views.process_mpesa_donation, name="mpesa_donation"),
    path('donate/bank/', views.process_bank_donation, name="bank_donation"),
]
