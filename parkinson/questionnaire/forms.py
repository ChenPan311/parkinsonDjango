from django import forms


class Question(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['answers'].help_text = '<li>על מנת לרשום תשובות כאופציה יש להפריד תשובות בפסיק , </li>'

    CHOICE_TYPE = (
        ('SingleChoice', 'בחירה יחידה'),
        ('MultipleChoice', 'בחירה מרובה'),
        ('OpenQuestion', 'שאלה פתוחה')
    )
    choice_type = forms.ChoiceField(choices=CHOICE_TYPE, label="סוג שאלה")
    title = forms.CharField(required=True,  widget=forms.TextInput(attrs={'placeholder': 'כתוב את השאלה'}) ,label="שאלה")

