from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog_home'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]