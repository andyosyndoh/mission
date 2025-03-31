from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Create your views here.
from .models import JobPost

class JobPostListView(ListView):
    model = JobPost
    template_name = 'careers.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        return JobPost.objects.filter(status='published').order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_jobs'] = JobPost.objects.filter(status='published')[:3]
        return context

class JobPostDetailView(DetailView):
    model = JobPost
    template_name = 'career-single.html'
    context_object_name = 'job'