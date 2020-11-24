from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .forms import Login, EmailBackend


# def user_login(response):
#     if response.method == "POST":
#         form = Login(response.POST)
#         if form.is_valid():
#             n = form.cleaned_data["username"]
#             p = form.cleaned_data["password"]
#             u = User(username=n, password=p)
#             u.save()
#             return HttpResponseRedirect("/%i" % u.id)
#     else:
#         print("else")
#         form = Login()
#     return render(response, "register/login.html", {"form": form})

def home(response):
    form = Login()
    if response.method == "GET":
        # if response.user.is_active:
        # return redirect("/myaccount")
        return render(response, "register/login.html", {"form": form})
    else:
        if response.method == "POST":
            form = Login(response.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(username=username, password=password)
                if user:
                    # if user.is_active:
                    #     login(response, user)
                    #     response.session['username'] = username
                    return redirect("/dashboard")  # here  we  need to send the dictinoary and puplate it
                else:
                    return render(response, "register/login.html",
                                  {"form": form, 'error': "Username and Password did not match"})


def dashboard(response):
    if response.method == "GET":
        return render(response, "dashboard/dashboard.html")
