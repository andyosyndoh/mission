from django.db import models
import uuid

class Donation(models.Model):
    CURRENCY_CHOICES = [
        ('KES', 'KES'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
    ]
    
    PURPOSE_CHOICES = [
        ('General Donation', 'General Donation'),
        ('Medical Equipment', 'Medical Equipment'),
        ('Patient Support', 'Patient Support'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    mpesa_number = models.CharField(max_length=15, blank=True, null=True)
    pesapal_transaction_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.full_name} - {self.amount} {self.currency}"