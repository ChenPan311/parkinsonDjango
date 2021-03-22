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


def get_medications_categories():
    MED_TYPE=()
    medications = get_medications()
    for med in medications.each():
        catergory_key=med.key()
        catergory_name=med.val()['categoryName']
        cat=(catergory_key,catergory_name),
        MED_TYPE+=cat
    return MED_TYPE



