import os
from pyrebase import pyrebase

config = {
    "apiKey": os.getenv("apiKey"),
    "authDomain": os.getenv("authDomain"),
    "databaseURL": os.getenv("databaseURL"),
    "storageBucket": os.getenv("storageBucket")
}

firebase = pyrebase.initialize_app(config)
auth_fb = firebase.auth()
db = firebase.database()


def get_questionnaire():
    questionnaire = db.child("Data").child('questionnaire_follow_up').get()
    return questionnaire


def get_medications():
    medications = db.child("Data").child('medicine_list').get()
    return medications


def get_medications_categories():  # Create a tuple of tuples for the use of MedicationForm
    MED_TYPE = ()
    medications = get_medications()
    for med in medications.each():
        category_key = med.key()
        category_name = med.val()['categoryName']
        cat = (category_key, category_name),
        MED_TYPE += cat
    return MED_TYPE


def get_medication_by_id(id):
    medications = get_medications()
    for category in medications.each():
        for key, val in category.val().get('medicationList').items():
            if key == id:
                return val.get('name')
