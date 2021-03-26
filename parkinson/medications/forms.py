from django import forms
import firebase_repo


class MedicationForm(forms.Form):
    def __init__(self, med_categories=None, *args, **kwargs):
        super(MedicationForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = med_categories

    category = forms.ChoiceField(choices=(), label="סוג תרופה")
    medication_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'שם התרופה'}),
                                      label="שם התרופה")
