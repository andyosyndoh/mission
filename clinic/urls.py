from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap  # 👈 Add this import
from .sitemaps import StaticViewSitemap, BlogSitemap

sitemaps = {
    'static': StaticViewSitemap(),
    'blog': BlogSitemap(),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clinicapp.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('careers/', include('careers.urls', namespace='careers')),
    # Corrected sitemap configuration 👇
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'clinicapp.views.custom_404'
handler500 = 'clinicapp.views.custom_500'
