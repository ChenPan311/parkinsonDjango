from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegisterForm,DoctorRegisterForm
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth


cred=credentials.Certificate('parkinsonhit.json')
firebase_admin.initialize_app(cred)

db=firestore.client()


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

            gender=doctor_form.cleaned_data["gender"]
            office_Phone=doctor_form.cleaned_data["Office_Phone"]
            mobile_Phone=doctor_form.cleaned_data["Mobile_Phone"]
            organization=doctor_form.cleaned_data["Organization"]

            user = auth.create_user(
                email=email,
                password=password,
                display_name=name,
                disabled=False
            )
            if(user):
                uid=user.uid
                db.collection('Doctors').document(uid).set({
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'gender':gender,
                    'office_Phone':office_Phone,
                    'mobile_Phone':mobile_Phone,
                    'organization':organization
                })
        else:
            return HttpResponse("Invalid")
        return redirect("/")
    else:
        form = RegisterForm()
        doctor_form=DoctorRegisterForm()
    return render(response, "register/register.html", {'form': form,'ourform':doctor_form})

