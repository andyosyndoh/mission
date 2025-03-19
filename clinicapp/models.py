from django.db import models
import uuid

# Create your models here.
class Appointment(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.date} {self.time}"
    
class TeamMember(models.Model):
    MEMBER_TYPE_CHOICES = [
        ('doctor', 'Doctor'),
        ('board', 'Board Member'),
    ]

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    member_type = models.CharField(max_length=10, choices=MEMBER_TYPE_CHOICES, default='doctor')
    bio = models.TextField()
    image = models.ImageField(upload_to='team/')
    is_featured = models.BooleanField(default=False)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_member_type_display()} - {self.name}"
    
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.email