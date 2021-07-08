from datetime import datetime
from django.views.decorators.cache import cache_control
from django.contrib import auth
from django.shortcuts import render, redirect
from firebase_repo import auth_fb, db, get_medications, get_medication_by_id
import PushService
from .forms import Login
from django.http import HttpResponse

DYSKINESIA = 6
ON = 4
OFF = 2
HALLUCINATION = 8
DOSAGES = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]


# Create your views here.

# Handles login users
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
            form.add_error('password', "אימייל או סיסמא אינם מתאימים!")
            return render(request, "register/login.html", {'form': form})


# Rendering home page
@cache_control(no_cache=False, must_revalidate=True, no_store=True)
def home(request):
    if request.method == "GET":
        if request.session.get('uid'):
            return render(request, "dashboard/dashboard.html")
        else:
            return redirect("/")


# Handles user logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    if request.session.get('uid') is not None:
        try:
            del request.session['uid']
            auth.current_user = None
            request.session.clear()
            return redirect("/")
        except KeyError:
            pass
    else:
        return redirect("/")


# Formatting the date given in ms
def prettydate(ms):
    date = datetime.fromtimestamp(ms / 1000.0)
    date = date.strftime('%d-%m-%Y %H:%M')
    return date


# Returns a list of reports objects
def status_data_for_chart(reports):
    reports_list = []

    if reports.val() is not None:
        for report in reports.each():
            label = prettydate(report.val().get('reportTime'))
            if report.val().get('hallucinations'):
                hallucination = 'True'
            else:
                hallucination = 'False'
            if report.val().get('falls'):
                falls = 'True'
            else:
                falls = 'False'
            if report.val().get('status') == "On":
                data = ON
            elif report.val().get('status') == "Off":
                data = OFF
            else:
                data = DYSKINESIA

            report_object = {
                'label': label,
                'value': data,
                'hallucinations': hallucination,
                'falls': falls
            }
            reports_list.append(report_object)
    return reports_list


# def medications_data_for_charts(medications):
#     report_list = []
#     if medications.val() is not None:
#         for medication in medications.each():
#             for time in medication.val()['hoursArr']:
#                 hour = str(time['hour']).rjust(2, '0')
#                 minutes = str(time['minutes']).rjust(2, '0')
#                 report_object = {
#                     'label': hour + ":" + minutes,
#                     'value': 8,
#                     'name': medication.val()['name']
#                 }
#                 report_list.append(report_object)
#     return report_list


# def medications_reports(medications_reports, patient_medications):
#     keys = []
#     data = []
#     for med_key in patient_medications.each():
#         keys.append(med_key.key())  # Creating keys arr for existing medications keys
#     if medications_reports.val() is not None:
#         for med_report in medications_reports.each():
#             for med in med_report.val():
#                 key = med.get('medicineId')
#                 if key in keys:
#                     med_name = patient_medications.val().get(key).get('name')
#                     report_object = {
#                         'label': prettydate(med.get('takenTime')),
#                         'name': med_name
#                     }
#                     data.append(report_object)
#     return data


# Returning a list of medicine reports object
def medications_reports(medications_reports):
    data = []
    if medications_reports.val() is not None:
        for med_report in medications_reports.each():
            name = ''
            for med in med_report.val():
                name += med.get('medicineName') + '\n'
                label = prettydate(med.get('takenTime'))

            report_object = {
                'label': label,
                'name': name
            }
            data.append(report_object)
    return data


# Patient page view, collecting all data
@cache_control(no_cache=False, must_revalidate=True, no_store=True)
def patient_detail(request):
    if request.session.get('uid') is not None:
        patient_id = request.GET.get("patient_id", 0)
        patients = db.child("Patients").order_by_child("id").equal_to(patient_id).get()
        if not patients.val():
            return render(request, "dashboard/dashboard.html", {'msg': "מטופל לא נמצא, נסה שנית"})
        for patient in patients.each():  # order_by returns a list
            request.session['patient_key'] = patient.key()
            patient_details = patient.val().get("user_details")
            patient_questionnaire = patient.val().get("questionnaire")
            patient_medications = db.child('Patients').child(patient.key()).child("medicine_list").get()
            patient_medications_reports = db.child('Patients').child(patient.key()).child("Medicine Reports").get()
            patient_reports = db.child('Patients').child(patient.key()).child("reports").get()
            patient_token = patient_details.get('token')
            request.session['patient_token'] = patient_token

            # Data for the charts
            reports = status_data_for_chart(patient_reports)
            reports_medication_list = medications_reports(patient_medications_reports)

            medications = get_medications()
            return render(request, "patient/patient_page.html", {'patient_details': patient_details,
                                                                 'patient_medications': patient_medications,
                                                                 'patient_questionnaire': patient_questionnaire,
                                                                 'reports': reports,
                                                                 'medications': medications,
                                                                 'medication_reports': reports_medication_list,
                                                                 'dosages': DOSAGES,
                                                                 'token': patient_token,
                                                                 })
    else:
        return redirect("/home")

# Checking if patient is exist
def patient_detail_check(request):
    patient_id = request.GET.get('data')
    exist = db.child("Patients").order_by_child('id').equal_to(patient_id).get()
    if exist.val():
        return HttpResponse("True")
    else:
        return HttpResponse("False")


# Updating patient's medicine from his data
def update_medicine(request):
    data = request.POST.dict()
    times = (data.get('hoursArr')).split(',')
    time_dict = {}
    idx = 0
    for time in times:
        if time != "00:00" and time != '':
            hours = time.split(':')[0]
            minutes = time.split(':')[1]
            time_dict[idx] = {'hour': int(hours), 'minutes': int(minutes)}
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
        db.child("Patients").child(request.session.get('patient_key')).child('user_details').child(
            "needToUpdateMedicine").set(False)
        PushService.send_medicine_notification(request.session.get('patient_token'))
        return HttpResponse("True")
    else:
        return HttpResponse("False")


# Deleting patient's medicine from his data
def delete_medicine(request):
    key_to_delete = request.POST.get('data')

    check = db.child("Patients").child(request.session.get('patient_key')).child('medicine_list') \
        .child(key_to_delete).remove()

    if check is None:
        is_empty = db.child("Patients").child(request.session.get('patient_key')).child('medicine_list').get()
        if is_empty:
            db.child("Patients").child(request.session.get('patient_key')).child('user_details').child(
            "needToUpdateMedicine").set(True)
        PushService.send_medicine_notification(request.session.get('patient_token'))
        return HttpResponse("True")
    else:
        return HttpResponse("False")

# def send_medication_notif(request):
#     result = PushService.send_medicine_notification(request.POST.get('data'))
#     if result['success'] == 1:
#         return HttpResponse('True')
#     else:
#         return HttpResponse('False')
#
#
# def send_questionnaire_notif(request):
#     result = PushService.send_questionnaire_notification(request.POST.get('data'))
#     if result['success'] == 1:
#         return HttpResponse('True')
#     else:
#         return HttpResponse('False')
