from django import forms
from django.core.validators import validate_email


class Login(forms.Form):
    email = forms.EmailField(required=True, validators=[validate_email], max_length=256, label='אימייל')
    password = forms.CharField(widget=forms.PasswordInput, label="סיסמא")
