from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Enrollment,Course
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = []
        
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'image', 'description', 'category']