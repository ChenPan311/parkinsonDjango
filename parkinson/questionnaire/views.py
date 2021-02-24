from django.shortcuts import render, redirect
from firebase_repo import db
from questionnaire.forms import Question



def question_create(request):
    form = Question()
    if request.method == "GET":
        return render(request, "questionnaire/questionnaire.html", {"question_form": form})

    if request.method == "POST":
        answers={}
        form = Question(request.POST)
        if form.is_valid():
            number_of_answers = int(request.POST.get("number_of_answers", 0))+1
            for i in range (number_of_answers):
                answers[str(i)]=request.POST.get(str(i))

            title=form.cleaned_data['title']
            choice_type=form.cleaned_data['choice_type']

            if choice_type=='SingleChoice' or choice_type== 'MultipleChoice' :
                type='MultipleChoiceQuestion'
            else:
                type = 'OpenQuestion'
            data={
                'title':title,
                'choiceType':choice_type,
                'choices':answers,
                'type':type
             }
            key = 0
            current_questionnaire=db.child("Data").child('questionnaire-test').child("questionList").get()
            if current_questionnaire.val() is not None:
                for question in current_questionnaire.each():
                    key=question.key()
                key+=1
            print(data)
            db.child("Data").child('questionnaire-test').child("questionList").child(str(key)).set(data)
        #     TODO:
            #remove/edit

