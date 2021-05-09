from django.urls import path
from registration import views as r_views

urlpatterns = [
    path('register/', r_views.register_new_doctor, name="register"),
    path('add_patient/', r_views.register_new_patient, name="add_patient"),
    path('add_patient/validate_details', r_views.validate_patient_details, name="add_patient"),

]
