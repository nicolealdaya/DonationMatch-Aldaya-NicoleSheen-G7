from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
   class Meta:
       model = CustomUser
       fields = [
           'full_name',
           'username',
           'email',
           'contact_number',
           'role',
       ]
       widgets = {
           'full_name': forms.TextInput(attrs={
               'placeholder': 'Enter your full name'
           }),
           'username': forms.TextInput(attrs={
               'placeholder': 'Enter your username'
           }),
           'email': forms.EmailInput(attrs={
               'placeholder': 'Enter your email'
           }),
           'contact_number': forms.TextInput(attrs={
               'placeholder': 'Enter your contact number'
           }),
           'role': forms.Select(),
       }