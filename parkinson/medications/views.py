import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from medications.forms import MedicationForm
from firebase_repo import get_medications, get_medications_categories, db


# Create your views here.


def medication_page(request):
    medications = get_medications()
    med_categories = get_medications_categories()
    medication_form = MedicationForm(med_categories)
    return render(request, "medications/medications.html", {"medication_form": medication_form,
                                                            "medications": medications})


def create_medicine(request):
    medicine_form = MedicationForm(med_categories=get_medications_categories(), data=request.POST)
    if medicine_form.is_valid():
        category = medicine_form.cleaned_data['category']
        medication_name = medicine_form.cleaned_data['medication_name']

        data = {
            'categoryId': category,
            'dosage': 0,
            'name': medication_name,
        }

        med_name = db.child("Data").child('medicine_list').child(category).child("medicationList").order_by_child(
            'name').equal_to(medication_name).get()

        if not med_name.val():
            db.child("Data").child('medicine_list').child(category).child("medicationList").push(data)
            return redirect('/medications')  # Reload new questionnaire and prevent resubmission
    return HttpResponse("Already Exist")


def check_if_med_exist(request):
    category = request.POST.get('dataString')
    # med_name = request.POST.get('med_name')
    print(category)

    # exist = db.child("Data").child('medicine_list').child(category).child("medicationList")\
    #     .order_by_child('name').equal_to(med_name).get()
    #
    # if exist.val():
    #     return HttpResponse("True")
    # else:
    #     return HttpResponse("False")
    # return HttpResponse("False")


def delete_medicine(request):
    med_to_delete = request.POST.get('key_to_delete', 0)
    category_key = str(med_to_delete).split(',')[0]
    medicine_key = str(med_to_delete).split(',')[1]
    db.child("Data").child('medicine_list').child(category_key).child("medicationList").child(medicine_key).remove()
    return redirect('/medications')


def edit_medicine(request):
    medicine_form = MedicationForm(med_categories=get_medications_categories(), data=request.POST)

    med_key_to_update = request.POST.get('key_to_edit', 0)
    if medicine_form.is_valid():
        category = medicine_form.cleaned_data['category']
        medication_name = medicine_form.cleaned_data['medication_name']
        data = {
            'categoryId': category,
            'dosage': 0,
            'name': medication_name,
        }

        med_name = db.child("Data").child('medicine_list').child(category).child("medicationList").order_by_child(
            'name').equal_to(medication_name).get()

        if not med_name.val():
            db.child("Data").child('medicine_list').child(category).child("medicationList").child(
                med_key_to_update).update(data)
            return redirect('/medications')  # Reload new questionnaire and prevent resubmission
    return HttpResponse("Already Exist")
