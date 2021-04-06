from datetime import datetime
from django.views.decorators.cache import cache_control
from django.contrib import auth
from django.shortcuts import render, redirect
from firebase_repo import auth_fb, db, get_medications
import PushService
from .forms import Login
from django.http import HttpResponse

DYSKINESIA = 6
ON = 4
OFF = 2
HALLUCINATION = 0


# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
            current_doctor_id = db.child("Doctors").child(user['localId']).child("details").get()
            name = current_doctor_id.val()['first_name'] + " " + current_doctor_id.val()['last_name']
            request.session['uid'] = str(user['idToken'])
            request.session['name'] = name
            request.session['email'] = user['email']
            return redirect("/home")
        except:
            message = "invalid cerediantials"
            return render(request, "register/login.html", {'msg': message, 'form': form})


@cache_control(no_cache=False, must_revalidate=True, no_store=True)
def home(request):
    if request.method == "GET":
        if request.session.get('uid'):
            return render(request, "dashboard/dashboard.html")
        else:
            return redirect("/")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    try:
        del request.session['uid']
        auth.current_user = None
        request.session.clear()
        return redirect("/")
    except KeyError:
        pass


def prettydate(ms):
    date = datetime.fromtimestamp(ms / 1000.0)
    date = date.strftime('%d-%m-%Y %H:%M:%S')
    return date


def status_data_for_chart(reports):
    reports_list = []
    if reports.val() is not None:
        for report in reports.each():
            label = prettydate(report.val()['reportTime'])
            if report.val()['hallucinations']:
                hallucination = 'True'
            else:
                hallucination = 'False'
            if report.val()['status'] == "On":
                data = ON
            elif report.val()['status'] == "Off":
                data = OFF
            else:
                data = DYSKINESIA

            report_object = {
                'label': label,
                'value': data,
                'hallucinations': hallucination
            }
            reports_list.append(report_object)
    return reports_list


def medications_data_for_charts(medications):
    report_list = []
    if medications.val() is not None:
        for medication in medications.each():
            for time in medication.val()['hoursArr']:
                hour = str(time['hour']).rjust(2, '0')
                minutes = str(time['minutes']).rjust(2, '0')
                report_object = {
                    'label': hour + ":" + minutes,
                    'value': 8,
                    'name': medication.val()['name']
                }
                report_list.append(report_object)
    return report_list


# @cache_control(no_cache=False, must_revalidate=True, no_store=True)
def patient_detail(request):
    patient_id = request.POST.get("patient_id", 0)
    patients = db.child("Patients").order_by_child("id").equal_to(patient_id).get()
    if not patients.val():
        return render(request, "dashboard/dashboard.html", {'msg': "מטופל לא נמצא, נסה שנית"})
    for patient in patients.each():  # order_by returns a list
        request.session['patient_key'] = patient.key()
        patient_details = patient.val().get("user_details")
        patient_questionnaire = patient.val().get("questionnaire")
        patient_medications = db.child('Patients').child(patient.key()).child("medicine_list").get()
        patient_reports = db.child('Patients').child(patient.key()).child("reports").get()
        patient_token = patient_details['token']

        # Data for the charts
        reports = status_data_for_chart(patient_reports)
        report_list = medications_data_for_charts(patient_medications)

        medications = get_medications()
        return render(request, "patient/patient_page.html", {'patient_details': patient_details,
                                                             'patient_medications': patient_medications,
                                                             'patient_questionnaire': patient_questionnaire,
                                                             'reports': reports,
                                                             'medications': medications,
                                                             'medication_reports': report_list,
                                                             'token': patient_token})


def patient_detail_check(request):
    patient_id = request.POST.get('data')
    exist = db.child("Patients").order_by_child('id').equal_to(patient_id).get()
    if exist.val():
        return HttpResponse("True")
    else:
        return HttpResponse("False")


def update_medicine(request):
    data = request.POST.dict()
    times = (data['hoursArr']).split(',')
    time_dict = {}
    idx = 0
    for time in times:
        if time != '':
            hours = int(time.split(':')[0])
            minutes = int(time.split(':')[1])
            time_dict[idx] = {'hour': hours, 'minutes': minutes}
            idx += 1

    data['hoursArr'] = time_dict
    data['dosage'] = float(data['dosage'])
    if data['keyToUpdate'] != data['id']:
        db.child("Patients").child(request.session.get('patient_key')).child('medicine_list').child(
            data['keyToUpdate']).remove()
    del data['keyToUpdate']
    check = db.child("Patients").child(request.session.get('patient_key')).child('medicine_list').child(
        data['id']).update(data)

    if check:
        return HttpResponse("True")
    else:
        return HttpResponse("False")


def delete_medicine(request):
    key_to_delete = request.POST.get('data')

    check = db.child("Patients").child(request.session.get('patient_key')).child('medicine_list') \
        .child(key_to_delete).remove()

    if check is None:
        return HttpResponse("True")
    else:
        return HttpResponse("False")


def send_medication_notif(request):
    result = PushService.send_medicine_notification(request.POST.get('data'))
    if result['success'] == 1:
        return HttpResponse('True')
    else:
        return HttpResponse('False')


def send_questionnaire_notif(request):
    result = PushService.send_questionnaire_notification(request.POST.get('data'))
    if result['success'] == 1:
        return HttpResponse('True')
    else:
        return HttpResponse('False')
