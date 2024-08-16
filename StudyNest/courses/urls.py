from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('course_category/', views.course_category, name='course_category'),
    path('courses/<str:foo>/', views.course_detail, name='course_detail'),
    path('lectures/<int:pk>/', views.lecture_detail, name='lecture_detail'),  # Updated URL pattern name
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('enrolled_courses/', views.enrolled_courses, name='enrolled_courses'), 
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    
   
    
]
