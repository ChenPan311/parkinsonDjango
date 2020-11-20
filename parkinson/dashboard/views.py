from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from .forms import Login


def user_login(response):
    if response.method == "POST":
        form = Login(response.POST)
        if form.is_valid():
            n = form.cleaned_data["username"]
            p = form.cleaned_data["password"]
            u = User(username=n, password=p)
            u.save()
            return HttpResponseRedirect("/%i" % u.id)
    else:
        print("else")
        form = Login()
    return render(response, "register/login.html", {"form": form})



