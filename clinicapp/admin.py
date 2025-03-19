from django.contrib import admin
from .models import Appointment, TeamMember

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