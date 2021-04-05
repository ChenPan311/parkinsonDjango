from django.urls import path
from medications import views as m_views

urlpatterns = [

    path('medications/', m_views.medication_page, name='medications'),
    path('medications/create/', m_views.create_medicine, name='medicine_creation'),
    path('medications/delete/', m_views.delete_medicine, name='delete_medicine'),
    path('medications/update/', m_views.edit_medicine, name='edit_medicine'),
    path('medications/check/', m_views.check_if_med_exist, name='medications_check'),

]
