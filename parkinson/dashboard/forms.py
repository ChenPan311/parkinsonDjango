from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import UserModel

class Login(ModelForm):
        password = forms.CharField(widget=forms.PasswordInput,label="סיסמא")
        class Meta:
            model = UserModel
            fields = "__all__"


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
                return user
        return None

    def get_user(self,uid):
        try:
            return User.objects.get(pk=uid)
        except:
            return None
