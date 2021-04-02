from django.urls import path

from dashboard import views as d_views
from registration import views as r_views
from questionnaire import views as q_views
from medications import views as m_views

urlpatterns = [
    path('', d_views.postsign, name="login"),
    path('register/', r_views.register_new_doctor, name="register"),
    path('add_patient/', r_views.register_new_patient, name="add_patient"),
    path('home/', d_views.home, name="home"),
    path('logout/', d_views.user_logout, name="logout"),
    path('patient_detail/', d_views.patient_detail, name="patient_detail"),
    path('patient_detail/med_update', d_views.update_medicine, name="patient_detail_update_med"),
    path('patient_detail/med_delete', d_views.delete_medicine, name="patient_detail_delete_med"),
    path('patient_detail/check', d_views.patient_detail_check, name="patient_detail"),
    path('patient_detail/send_medication_notif', d_views.send_medication_notif, name="send_medication_notification"),
    path('questionnaire/', q_views.questionnaire_page, name='questionnaire'),
    path('questionnaire/create/', q_views.create_question, name='question_creation'),
    path('questionnaire/delete/', q_views.delete_question, name='delete_question'),
    path('questionnaire/update/', q_views.edit_question, name='edit_question'),
    path('medications/', m_views.medication_page, name='medications'),
    path('medications/create/', m_views.create_medicine, name='medicine_creation'),
    path('medications/delete/', m_views.delete_medicine, name='delete_medicine'),
    path('medications/update/', m_views.edit_medicine, name='edit_medicine'),
    path('medications/check/', m_views.check_if_med_exist, name='medications_check'),


]
