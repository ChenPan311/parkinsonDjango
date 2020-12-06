from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm,DoctorRegisterForm
from django.contrib import auth
from google.cloud import firestore
import pyrebase

config = {
   "apiKey": "AIzaSyClOwdD-d0Ex6KK1pajH-6NU0SlnlPicO4",
   "authDomain": "parkinsonhit-1ac54.firebaseapp.com",
   "databaseURL": "https://parkinsonhit-1ac54.firebaseio.com",
   "projectId": "parkinsonhit-1ac54",
   "storageBucket":"parkinsonhit-1ac54.appspot.com",
   "messagingSenderId": "155781604374",
   "appId": "1:155781604374:web:b3d4d411ae691c14e10137",
   "measurementId": "G-T6N1PP9BHW"
}

firebase = pyrebase.initialize_app(config)

auth_fb = firebase.auth()
db = firestore.Client()


# Create your views here.

def register_new_doctor(response):
    if response.method == "POST":
        django_form = RegisterForm(response.POST)#django User
        doctor_form=DoctorRegisterForm(response.POST)#our user
        if django_form.is_valid() and doctor_form.is_valid():
            first_name=django_form.cleaned_data["first_name"]
            last_name=django_form.cleaned_data["last_name"]
            name=first_name+" "+last_name
            email=django_form.cleaned_data["email"]
            password=django_form.cleaned_data["password1"]
            user=auth_fb.create_user_with_email_and_password(email,password)
            uid=user["localId"]
            data={"name":name}
            # user=django_form.save()
            # user.save()
            # profile=doctor_form.save(commit=False)
            # profile.user=user
            # profile.save()
        else:
            return HttpResponse("Invalid")
        return redirect("/")
    else:
        form = RegisterForm()
        doctor_form=DoctorRegisterForm()
    return render(response, "register/register.html", {'form': form,'ourform':doctor_form})

