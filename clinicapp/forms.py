from django import forms
from .models import Appointment, Subscriber, Contact

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['full_name', 'email', 'date', 'time', 'message']

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