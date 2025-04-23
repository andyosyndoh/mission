from django import forms
from .models import Appointment, Subscriber, Contact
from django.forms.widgets import TextInput

class BaseAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['full_name', 'email', 'department', 'date', 'time', 'phone', 'message']

    # Override the default widgets for date/time fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = TextInput(attrs={
            'class': 'form-control flatpickr-date',
            'placeholder': 'Select Date',
        })
        self.fields['time'].widget = TextInput(attrs={
            'class': 'flatpickr-time',
            'placeholder': 'Select Time',
        })

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            })
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Message',
                'rows': 7,
                'cols': 30
            }),
        }