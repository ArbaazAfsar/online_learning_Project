from django import forms
from .models import Question, Choice,Quiz

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
            
            
            
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course', 'title', 'description', 'total_marks', 'passing_marks']
        

class QustionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
