from django.urls import include, path
from .import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('services', views.services, name="services"),
    path('doctors', views.doctors, name="doctors"),
    path('contact', views.contact, name="contact"),
    path('appointment/', views.book_appointment, name="appointment"),    
    path("mpesa/stkpush/", views.initiate_payment, name="mpesa_stkpush"),
    path('donation/', views.donation_view, name='donation'),
]
