from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Enrollment,Course,CourseCategory,Lecture
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
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        fields = ['name', 'image']
        
        
class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'description', 'video_url', 'video_file', 'order']
