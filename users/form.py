from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class RegisterCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email' , 'username' , 'contact']

class UpdateCustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image' , 'contact']

class UpdatePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']
        