from django.contrib import admin

# Register your models here.
from .models import JobPost

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'job_type', 'application_deadline', 'status')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'job_type', 'location')
    date_hierarchy = 'application_deadline'