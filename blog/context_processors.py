from .models import Post, Category, Tag

def shared_context(request):
    return {
        'recent_posts': Post.objects.filter(status='published')[:3],
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }