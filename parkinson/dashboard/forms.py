from django import forms
from firebase_repo import db
from django.core.validators import validate_email


class Login(forms.Form):
    email = forms.EmailField(required=True, validators=[validate_email], max_length=256, label='אימייל')
    password = forms.CharField(widget=forms.PasswordInput, label="סיסמא")


# class Medications(forms.Form):
#     category_list = []
#     sub_catgories = []
#     patient_medications = db.child('Data').child('medicine_list').get()
#     for medication in patient_medications.each():
#         category_list.append(medication.val()["categoryName"])
#         sub_medications = db.child('Data').child('medicine_list').child(medication.key()).child('medicationList').get()
#         med_list = []
#         for med in sub_medications.each():
#             med_list.append(med.val()["categoryName"])
#     sub_catgories.append(med_list)
