from django.http import HttpResponse
from django.shortcuts import render, redirect
from firebase_repo import auth_fb, db
from .forms import RegisterForm, DoctorRegisterForm, PatientRegisterForm


# Create your views here.

def register_new_doctor(response):
    if response.method == "POST":
        django_form = RegisterForm(response.POST)  # django User
        doctor_form = DoctorRegisterForm(response.POST)  # our user
        if django_form.is_valid() and doctor_form.is_valid():
            first_name = django_form.cleaned_data["first_name"]
            last_name = django_form.cleaned_data["last_name"]
            email = django_form.cleaned_data["email"]
            password = django_form.cleaned_data["password1"]
            gender = doctor_form.cleaned_data["gender"]
            office_phone = doctor_form.cleaned_data["office_phone"]
            mobile_phone = doctor_form.cleaned_data["mobile_phone"]
            organization = doctor_form.cleaned_data["organization"]
            doctor = auth_fb.create_user_with_email_and_password(email=email, password=password)
            if doctor:
                data = {
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'gender': gender,
                    'office_phone': office_phone,
                    'mobile_phone': mobile_phone,
                    'organization': organization,
                }
                db.child("Doctors").child(doctor['localId']).child("details").set(data)
        else:
            return HttpResponse("Invalid")
        return redirect("/")
    else:
        form = RegisterForm()
        doctor_form = DoctorRegisterForm()
    return render(response, "register/register.html", {'form': form, 'ourform': doctor_form})


def register_new_patient(response):
    if response.method == "POST":
        django_form = RegisterForm(response.POST)  # django User
        patient_form = PatientRegisterForm(response.POST)  # our user
        if django_form.is_valid() and patient_form.is_valid():
            first_name = django_form.cleaned_data["first_name"]
            last_name = django_form.cleaned_data["last_name"]
            email = django_form.cleaned_data["email"]
            password = django_form.cleaned_data["password1"]

            gender = patient_form.cleaned_data["gender"]
            country = patient_form.cleaned_data["country"]
            mobile_phone = patient_form.cleaned_data["mobile_phone"]
            HMO = patient_form.cleaned_data["HMO"]
            date_of_birth = patient_form.cleaned_data['date_of_birth']
            patient = auth_fb.create_user_with_email_and_password(email=email, password=password)

            if patient:
                data = {
                    'doctor': response.session.get('email'),
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'gender': gender,
                    'mobile_phone': mobile_phone,
                    'HMO': HMO,
                    'country': country,
                    'date_of_birth': str(date_of_birth)
                }
                db.child("Django-Patients").child(patient['localId']).child("details").set(data)
        else:
            return HttpResponse("Invalid")
        return redirect("/home")
    else:
        if response.session.get('uid') is not None:
            form = RegisterForm()
            patient_form = PatientRegisterForm()
            return render(response, "register/add_new_patient.html", {'form': form, 'ourform': patient_form})
        else:
            return redirect("/")
