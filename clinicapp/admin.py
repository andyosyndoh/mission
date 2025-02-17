from django.contrib import admin
from .models import Appointment, Doctor

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'date', 'time', 'created_at')
    search_fields = ('full_name', 'email')
    list_filter = ('date',)

    def has_add_permission(self, request):
        return False
    
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_featured')
    list_editable = ('is_featured',)
    search_fields = ('name', 'position')
    list_filter = ('position',)