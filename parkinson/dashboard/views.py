from datetime import datetime

from django.contrib import auth
from django.shortcuts import render, redirect
from firebase_repo import auth_fb, db
from .forms import Login


# Create your views here.

def postsign(request):
    form = Login()
    email, password = None, None
    if request.method == "GET":
        if request.session.get('uid') is not None:
            return redirect("/home", )
        return render(request, "register/login.html", {"form": form})

    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
    try:
        user = auth_fb.sign_in_with_email_and_password(email, password)
        request.session['uid'] = str(user['idToken'])
        current_doctor_id = db.child("Doctors").child(user['localId']).child("details").get()
        name = current_doctor_id.val()['first_name'] + " " + current_doctor_id.val()['last_name']
        request.session['name'] = name
        request.session['email'] = user['email']
        return redirect("/home", )
    except:
        message = "invalid cerediantials"
        return render(request, "register/login.html", {'msg': message, 'form': form})


def home(request):
    msg = request.GET.get('msg')
    if request.method == "GET":
        print(request.session.get('uid'))
        if request.session.get('uid'):
            name = request.session.get('name')
            return render(request, "dashboard/dashboard.html", {'name': name})
        else:
            print("got to else")
            print(msg)
            return render(request, "register/login.html", {'msg': msg})


def user_logout(request):
    try:
        del request.session['uid']
        auth.current_user = None

        request.session.clear()
        return redirect("/")
    except KeyError:
        pass


def patient_detail(request):
    patient_id = request.POST.get("patient_id", 0)
    name = request.session.get('name')
    patients = db.child("Patients").order_by_child("id").equal_to(patient_id).get()
    if not patients.val():
        return render(request, "dashboard/dashboard.html", {'name': name, 'msg': "מטופל לא נמצא, נסה שנית"})
    for patient in patients.each():  # order_by returns a list
        patient_details = patient.val()["user_details"]
        patient_questionnaire = patient.val()["questionnaire"]
        patient_medications = db.child('Patients').child(patient.key()).child("medicine_list").get()
        patient_reports = db.child('Patients').child(patient.key()).child("reports").get()


        # print(patient_medications1)

        for field in patient_details:
            if field == 'birthDate':
                print(patient_details[field]['time'])
            else:
                print(patient_details[field])

        return render(request, "patient/patient_page.html", {'patient_details': patient_details,
                                                             'patient_medications': patient_medications,
                                                             'patient_questionnaire': patient_questionnaire,
                                                             'patient_reports': patient_reports,
                                                             'name': name})
