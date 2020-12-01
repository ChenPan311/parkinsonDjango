from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth

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

# Create your views here.
from .forms import Login, EmailBackend


def postsign(request):
    form = Login()
    email, password = None, None
    if request.method == "GET":
        return render(request, "register/login.html", {"form": form})

    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
    try:
        user = auth_fb.sign_in_with_email_and_password(email, password)
    except:
        message = "invalid cerediantials"
        return render(request, "register/login.html",{'msg':message,'form':form})

    if (user):
        request.session['uid']=str(user['localId'])
        return render(request,"dashboard/dashboard.html",{'email':email})


def home(response):
    form = Login()

    if response.method == "GET":
        if response.user.is_active:
            return redirect("/dashboard")
        return render(response, "register/login.html", {"form": form})
    else:
        if response.method == "POST":
            form = Login(response.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(response, user)
                        response.session['username'] = username
                    return redirect("/dashboard")  # here  we  need to send the dictinoary and puplate it
                else:
                    return render(response, "register/login.html",
                                  {"form": form, 'error': "Username and Password did not match"})


@login_required
def dashboard(request):
    if request.method == "GET":
        return render(request, "dashboard/dashboard.html", )


def user_logout(request):
    print("hello")
    auth.logout(request)
    return redirect("/")
