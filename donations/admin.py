from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'currency', 'payment_status', 'created_at')
    search_fields = ('name', 'email', 'transaction_ref')
    list_filter = ('payment_status', 'payment_method')

