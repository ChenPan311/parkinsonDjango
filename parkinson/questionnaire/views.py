from django.shortcuts import render, redirect
from firebase_repo import db, get_questionnaire, get_medications
from questionnaire.forms import Question
import time


def questionnaire_page(request):
    if request.session.get('uid') is not None:
        questionnaire = get_questionnaire()
        form = Question()
        return render(request, "questionnaire/questionnaire.html", {"question_form": form,
                                                                    "questionnaire": questionnaire})
    else:
        return redirect("/home", )


def create_question(request):
    if request.method == "POST":
        answers = {}
        form = Question(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            choice_type = form.cleaned_data['choice_type']
            if choice_type != 'OpenQuestion':
                number_of_answers = int(request.POST.get("number_of_answers", 0)) + 1
                for i in range(number_of_answers):
                    answers[str(i)] = request.POST.get(str(i))

            if choice_type == 'SingleChoice' or choice_type == 'MultipleChoice':
                type = 'MultipleChoiceQuestion'
            else:
                type = 'OpenQuestion'
            data = {
                'title': title,
                'choiceType': choice_type,
                'choices': answers,
                'type': type
            }
            db.child("Data").child('questionnaire_follow_up').child("questionList").push(data)
            db.child("Data").child('questionnaire_follow_up').child("answeredAt").update(
                {'time': round(time.time() * 1000)})
            return redirect('/questionnaire')  # Reload new questionnaire and prevent resubmission


def delete_question(request):
    question_to_delete = request.POST.get('key_to_delete', 0)
    db.child("Data").child('questionnaire_follow_up').child("questionList").child(question_to_delete).remove()
    return redirect('/questionnaire')


def edit_question(request):
    question_to_edit = request.POST.get('key_to_edit', 0)
    if request.method == "POST":
        answers = {}
        form = Question(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            choice_type = form.cleaned_data['choice_type']
            if choice_type != 'OpenQuestion':
                number_of_answers = int(request.POST.get("edit_number_of_answers", 0)) + 1
                for i in range(number_of_answers):
                    answers[str(i)] = request.POST.get(str(i))

            if choice_type == 'SingleChoice' or choice_type == 'MultipleChoice':
                type = 'MultipleChoiceQuestion'
            else:
                type = 'OpenQuestion'
            data = {
                'title': title,
                'choiceType': choice_type,
                'choices': answers,
                'type': type
            }
            db.child("Data").child('questionnaire_follow_up').child("questionList").child(question_to_edit).update(data)
            db.child("Data").child('questionnaire_follow_up').child("answeredAt").update(
                {'time': round(time.time() * 1000)})
    return redirect('/questionnaire')  # Reload new questionnaire and prevent resubmission
