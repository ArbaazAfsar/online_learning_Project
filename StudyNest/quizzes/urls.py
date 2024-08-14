from django.urls import path
from . import views

urlpatterns = [
    path('courses/<int:course_id>/quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('courses/<int:course_id>/quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    path('courses/<int:course_id>/quiz/<int:quiz_id>/retry/', views.retry_quiz, name='retry_quiz'),
]