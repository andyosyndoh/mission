from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post  # Import your blog model if you have one

class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return ['home', 'about','services','team','contact']  # Add other static pages from your URLs

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    """Sitemap for dynamic blog posts"""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.publish_date  # Ensure your Post model has an 'updated_at' field
