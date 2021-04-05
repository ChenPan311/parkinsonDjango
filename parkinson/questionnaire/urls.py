from django.urls import path
from questionnaire import views as q_views

urlpatterns = [
    path('questionnaire/', q_views.questionnaire_page, name='questionnaire'),
    path('questionnaire/create/', q_views.create_question, name='question_creation'),
    path('questionnaire/delete/', q_views.delete_question, name='delete_question'),
    path('questionnaire/update/', q_views.edit_question, name='edit_question'),

]
