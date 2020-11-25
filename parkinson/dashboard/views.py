from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .forms import Login, EmailBackend


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


@login_required
def user_logout(request):
    logout(request)
    return redirect("/")
