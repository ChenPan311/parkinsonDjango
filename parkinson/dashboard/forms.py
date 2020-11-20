from django import forms
from django.forms import ModelForm
from .models import UserModel

class Login(ModelForm):
        password = forms.CharField(widget=forms.PasswordInput)

        class Meta:
            model = UserModel
            fields = "__all__"

