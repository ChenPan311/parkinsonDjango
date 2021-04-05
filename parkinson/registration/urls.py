from django.urls import path
from registration import views as r_views

urlpatterns = [
    path('register/', r_views.register_new_doctor, name="register"),
    path('add_patient/', r_views.register_new_patient, name="add_patient"),

]
