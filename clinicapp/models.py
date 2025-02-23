from django.db import models
from django.utils import timezone

# Existing Models
class Appointment(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.date} {self.time}"

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='doctors/')
    is_featured = models.BooleanField(default=False)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    google_plus = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

# Donation Model
class Donation(models.Model):
    PAYMENT_METHODS = (
        ('BANK', 'Bank Transfer'),
        ('MPESA', 'M-Pesa'),
    )
    
    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')  # KES for Kenyan Shilling
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    donor_name = models.CharField(max_length=100)
    donor_email = models.EmailField()
    donor_country = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.donor_name} - {self.amount} {self.currency}"