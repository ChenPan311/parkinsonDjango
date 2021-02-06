from django.urls import path

from dashboard import views as d_views
from registration import views as r_views

urlpatterns = [
    path('', d_views.postsign, name="login"),
    path('register/', r_views.register_new_doctor, name="register"),
    path('add_patient/', r_views.register_new_patient, name="add_patient"),
    path('home/', d_views.home, name="home"),
    path('logout/', d_views.user_logout, name="logout"),
    path('patient_detail/', d_views.patient_detail, name="patient_detail"),

]
