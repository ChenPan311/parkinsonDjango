from django.http import HttpResponse
from django.shortcuts import render, redirect
from urlparams.redirect import param_redirect

from .forms import RegisterForm, DoctorRegisterForm,PatientRegisterForm
from dashboard.forms import Login
from firebase_admin import credentials
from firebase_repo import auth_fb,db
# cred=credentials.Certificate('parkinsonhit.json')
# firebase_admin.initialize_app(cred)




# .document(u'alovelace')
# doc_ref.set({
#     u'first': u'Ada',
#     u'last': u'Lovelace',
#     u'born': 1815
# })


# user = auth.create_user(
#     email='user@example.com',
#     email_verified=False,
#     phone_number='+15555550100',
#     password='secretPassword',
#     display_name='John Doe',
#     photo_url='http://www.example.com/12345678/photo.png',
#     disabled=False)
# print('Sucessfully created new user: {0}'.format(user.uid))

# Create your views here.

def register_new_doctor(response):
    if response.method == "POST":
        django_form = RegisterForm(response.POST)  # django User
        doctor_form = DoctorRegisterForm(response.POST)  # our user
        if django_form.is_valid() and doctor_form.is_valid():
            first_name = django_form.cleaned_data["first_name"]
            last_name = django_form.cleaned_data["last_name"]
            # name = first_name + " " + last_name
            email = django_form.cleaned_data["email"]
            password = django_form.cleaned_data["password1"]

            gender = doctor_form.cleaned_data["gender"]
            office_Phone = doctor_form.cleaned_data["Office_Phone"]
            mobile_Phone = doctor_form.cleaned_data["Mobile_Phone"]
            organization = doctor_form.cleaned_data["Organization"]
            doctor = auth_fb.create_user_with_email_and_password(email=email,password=password)
            if (doctor):
                data={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'gender': gender,
                    'office_Phone': office_Phone,
                    'mobile_Phone': mobile_Phone,
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


def register_new_Patient(response):
    if response.method == "POST":
        django_form = RegisterForm(response.POST)  # django User
        patient_form = PatientRegisterForm(response.POST)  # our user
        if django_form.is_valid() and patient_form.is_valid():
            first_name = django_form.cleaned_data["first_name"]
            last_name = django_form.cleaned_data["last_name"]
            # name = first_name + " " + last_name
            email = django_form.cleaned_data["email"]
            password = django_form.cleaned_data["password1"]

            # gender = doctor_form.cleaned_data["gender"]
            # office_Phone = doctor_form.cleaned_data["Office_Phone"]
            country=patient_form.cleaned_data["Country"]
            mobile_Phone = patient_form.cleaned_data["Mobile_Phone"]
            HMO = patient_form.cleaned_data["HMO"]
            patient = auth_fb.create_user_with_email_and_password(email=email,password=password)

            print(response.session.get('email'))
            if (patient):
                data={
                    'Doctor':response.session.get('email'),
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    # 'gender': gender,
                    # 'office_Phone': office_Phone,
                    'mobile_Phone': mobile_Phone,
                    'HMO': HMO,
                    'Country':country

                }

                db.child("Patients").child(patient['localId']).child("details").set(data)
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


