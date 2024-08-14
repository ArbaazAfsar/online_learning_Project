from django.urls import path
from . import views

urlpatterns = [
    path('courses/<int:course_id>/quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('courses/<int:course_id>/quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    path('courses/<int:course_id>/quiz/<int:quiz_id>/retry/', views.retry_quiz, name='retry_quiz'),
    path('upload/quiz/', views.upload_quiz, name='upload_quiz'),
    path('quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),
]