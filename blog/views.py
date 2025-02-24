from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag

class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'
    paginate_by = 6  # Matches template's 6 posts per page

    def get_queryset(self):
        return Post.objects.filter(status='published').order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.filter(status='published')[:3]
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog-single.html'
    context_object_name = 'post_detail'