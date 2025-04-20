from django import forms
from .models import ContactMessage
from django.core.exceptions import ValidationError


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message', 'rows': 7}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@example.com'):
            raise ValidationError("Email must be from the domain 'example.com'")
        return email

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        if len(message) < 10:  # Now safe for None/empty strings
            raise forms.ValidationError("Message too short (min 10 chars)")
        return message