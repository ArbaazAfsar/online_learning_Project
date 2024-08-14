from django import forms
from .models import Question, Choice

class QuizAttemptForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizAttemptForm, self).__init__(*args, **kwargs)
        
        for question in questions:
            choices = [(choice.id, choice.choice_text) for choice in question.choices.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label=question.question_text
            )
