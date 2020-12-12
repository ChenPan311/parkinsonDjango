from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.validators import validate_email

from registration.models import Doctor

class Login(forms.Form):
        email=forms.EmailField(required=True,validators=[validate_email],max_length=256,label='אימייל')
        password = forms.CharField(widget=forms.PasswordInput,label="סיסמא")



# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         try:
#             user = UserModel.objects.get(email=username)
#         except UserModel.DoesNotExist:
#             return None
#         if user.check_password(password):
#                 return user
#         return None
#
#     def get_user(self,uid):
#         try:
#             return User.objects.get(pk=uid)
#         except:
#             return None
