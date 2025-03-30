from django.contrib import admin
from .models import Appointment, TeamMember, Testimonial

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'date', 'time', 'created_at')
    search_fields = ('full_name', 'email')
    list_filter = ('date',)

    def has_add_permission(self, request):
        return False
    
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'member_type', 'is_featured')
    list_filter = ('member_type', 'is_featured',)
    search_fields = ('name', 'position')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'active', 'order', 'created_at')
    list_editable = ('active', 'order')
    search_fields = ('name', 'position', 'content')
    list_filter = ('active', 'created_at')
    fields = ('name', 'position', 'content', 'image', 'active', 'order')