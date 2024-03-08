from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from django.core.exceptions import ValidationError

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
        
class SetNewPasswordForm (forms.Form ) :
    password = forms.CharField(widget=forms.PasswordInput , label='old password')
    password1 = forms.CharField(widget=forms.PasswordInput , label='new password')
    password2 = forms.CharField(widget=forms.PasswordInput , label='new password repeat')

    def clean(self) :
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2 :
            raise ValidationError("password e reapet ba asli yeki nis ")