from django.db import models
import uuid

# Create your models here.
class Appointment(models.Model):
    DEPARTMENT_CHOICES = [
        ('Consultation', 'Consultation'),
        ('Medical Services', 'Medical Services'),
        ('Surgical Services', 'Surgical Services'),
        ('Critical Care Services', 'Critical Care Services'),
        ('Laboratory Investigations', 'Laboratory Investigations'),
        ('Maternity Services', 'Maternity Services'),
        ('Maternal and Child Health Services', 'Maternal and Child Health Services'),
        ('HIV and TB Services', 'HIV and TB Services'),
        ('Ambulance Services', 'Ambulance Services'),
        ('Ultrasound', 'Ultrasound'),
        ('Special Clinics (MOPC, GOPC, SOPC)', 'Special Clinics (MOPC, GOPC, SOPC)'),
        ('New Born Unit', 'New Born Unit'),
    ]
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    department = models.CharField(max_length=255, choices=DEPARTMENT_CHOICES, blank=True)
    date = models.DateField()
    time = models.TimeField()
    phone = models.CharField(max_length=20, blank=True)
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
    
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/')
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.position}"
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.name}"