from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Enrollment,Course,CourseCategory,Lecture,Review
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


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
        fields = ['title', 'description', 'video_file', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lecture Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Lecture Description'}),
            # 'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Video URL'}),
            'video_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Order'}),
        }
        
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }
    
    rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
    )
