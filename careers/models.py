from django.db import models
from django.urls import reverse
# Create your models here.
class JobPost(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    JOB_TYPE_CHOICES = (
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    description = models.TextField()
    requirements = models.TextField()
    application_deadline = models.DateField()
    publish_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    def get_absolute_url(self):
        return reverse('careers:job_detail', args=[self.slug])

    def __str__(self):
        return self.title