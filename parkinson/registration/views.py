from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm,DoctorRegisterForm

# Create your views here.

def register_new_doctor(response):
    if response.method == "POST":
        django_form = RegisterForm(response.POST)#django User
        doctor_form=DoctorRegisterForm(response.POST)#our user
        if django_form.is_valid() and doctor_form.is_valid():
            user=django_form.save()
            user.save()
            profile=doctor_form.save(commit=False)
            profile.user=user
            profile.save()
        else:
            return HttpResponse("Invalid")
        return redirect("/")
    else:
        form = RegisterForm()
        doctor_form=DoctorRegisterForm()
    return render(response, "register/register.html", {'form': form,'ourform':doctor_form})

