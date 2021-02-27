from django.shortcuts import render, redirect
from firebase_repo import db, get_questionnaire
from questionnaire.forms import Question


def create_question(request):
    questionnaire = get_questionnaire()
    form = Question()
    if request.method == "GET":
        return render(request, "questionnaire/questionnaire.html", {"question_form": form,
                                                                    "questionnaire": questionnaire})
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
            # key = 0
            # if questionnaire.val() is not None:
            #     for question in questionnaire.each():
            #         key = question.key()
            #     key += 1
            db.child("Data").child('questionnaire_follow_up_test').child("questionList").push(data)

            return redirect('/questionnaire')  # Reload new questionnaire and prevent resubmission


def delete_question(request):
    question_to_delete = request.POST.get('key_to_delete', 0)
    db.child("Data").child('questionnaire_follow_up_test').child("questionList").child(question_to_delete).remove()
    return redirect('/questionnaire')
    # print(question_to_delete)


def edit_question(request):
    question_to_edit = request.POST.get('key_to_edit', 0)
    return None