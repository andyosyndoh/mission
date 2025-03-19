from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('services', views.services, name="services"),
    path('team', views.team, name="team"),
    path('contact', views.contact, name="contact"),
    path('appointment/', views.book_appointment, name="appointment"),
    path('subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('confirm/<uuid:token>/', views.confirm_subscription, name='confirm_subscription'),
]
