from django.db import models

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