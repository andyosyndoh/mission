from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('', views.JobPostListView.as_view(), name='careers_list'),
    path('<slug:slug>/', views.JobPostDetailView.as_view(), name='job_detail')
]