from django import forms
from .models import User


class UserForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': '',
            "placeholder": "Eg. John-2755"
        }
    ))
    email = forms.CharField(required=True, widget=forms.EmailInput(
        attrs={
            'class': '',
            "placeholder": "name@example.com"
        }
    ))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': '',
            "placeholder": "***************"
        }
    ))
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(
        attrs={
            'class': '',
            "placeholder": "***************"
        }
    ))


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
