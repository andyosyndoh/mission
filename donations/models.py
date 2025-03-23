from django.db import models
import uuid
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator



# Create your models here.
class Donation(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('mpesa', 'M-Pesa'),
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('other', 'Other'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    transaction_ref = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mpesa_message = models.CharField(max_length=255, blank=True, null=True)  # For M-Pesa prompt message
    
    def __str__(self):
        return f"{self.name} - {self.amount} {self.currency}"
    
amount = models.DecimalField(
    max_digits=10, 
    decimal_places=2, 
    validators=[MinValueValidator(0.01)]  # Ensure amount is greater than 0
)

phone_number = models.CharField(
    max_length=20, 
    blank=True, 
    null=True,
    validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be in the format: '+254700000000'."
        )
    ]
)