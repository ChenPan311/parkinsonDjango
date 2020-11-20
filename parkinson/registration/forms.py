from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Doctor

class RegisterForm(UserCreationForm):#django registration form
    class Meta:
        model = User
        fields = ("username", "email","password1","password2","first_name","last_name")

class DoctorRegisterForm(forms.ModelForm):
    class Meta:
        model=Doctor
        labels={
            "Office_Phone": "Office Phone",
            "Mobile_Phone": "Mobile Phone",
    }
        exclude=('user',)