from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Post, Category, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'status')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'categories')

admin.site.register(Category)
admin.site.register(Tag)