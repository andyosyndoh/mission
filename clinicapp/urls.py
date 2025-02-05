from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about.html', views.about, name="about"),
    path('services.html', views.services, name="services"),
    path('doctors.html', views.doctors, name="doctors"),
    path('contact.html', views.contact, name="contact"),
    path('blog/', include('blog.urls', namespace='blog')),
]
