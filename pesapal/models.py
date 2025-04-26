from django.db import models
from django.contrib.auth.models import User
import uuid

class PesapalTransaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    order_id = models.UUIDField(default=uuid.uuid4, unique=True)
    pesapal_id = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    donation_purpose = models.CharField(max_length=100, default='General Donation')
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Add this line

    def __str__(self):
        return f"{self.order_id} - {self.amount} {self.currency}"