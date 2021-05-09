from django.http import HttpResponse
from django.shortcuts import render, redirect
from firebase_repo import auth_fb, db, check_if_patient_exists, check_if_doctor_exists
from datetime import datetime
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
            return render(response, "register/register.html", {'form': django_form, 'ourform': doctor_form})
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
            clinic = patient_form.cleaned_data["clinic"]
            date_of_birth = str(patient_form.cleaned_data['date_of_birth'])
            patient = auth_fb.create_user_with_email_and_password(email=email, password=password)

            epoch = datetime(1970, 1, 1)
            dt_obj = datetime.strptime(date_of_birth, '%Y-%m-%d')
            if dt_obj > epoch:
                millisec = dt_obj.timestamp() * 1000
            else:
                millisec = (dt_obj - epoch).total_seconds() * 1000
            data = {
                'doctor': response.session.get('email'),
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'gender': gender,
                'mobile_phone': mobile_phone,
                'clinic': clinic,
                'country': country,
                'hasUnansweredQuestionnaire': True,
                'needToUpdateMedicine': True,
                'date_of_birth': millisec,
                'token': ''
            }
            db.child("Patients").child(patient['localId']).set({'id': mobile_phone})
            db.child("Patients").child(patient['localId']).child("user_details").set(data)
        else:
            return render(response, "register/add_new_patient.html", {'form': django_form, 'ourform': patient_form})
        return redirect("/home")
    else:  # Get
        if response.session.get('uid') is not None:
            form = RegisterForm()
            patient_form = PatientRegisterForm()
            return render(response, "register/add_new_patient.html", {'form': form, 'ourform': patient_form})
        else:
            return redirect("/")


def validate_email(request):
    email = request.POST.get('email')
    is_patient = request.POST.get('isPatient') == 'true'
    if email == '':
        return HttpResponse("FillEmail")
    if is_patient:
        if check_if_patient_exists(email):
            return HttpResponse("EmailExists")
    else:
        if check_if_doctor_exists(email):
            return HttpResponse("EmailExists")
    return HttpResponse("Valid")
