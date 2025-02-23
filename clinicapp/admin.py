from django.contrib import admin
from .models import Appointment, Doctor, Donation

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

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'amount', 'currency', 'payment_method', 'status', 'created_at')
    search_fields = ('donor_name', 'donor_email', 'transaction_id')
    list_filter = ('payment_method', 'status', 'created_at')
    readonly_fields = ('created_at', 'completed_at')

    def has_add_permission(self, request):
        return False  # Disable adding donations from the admin interface