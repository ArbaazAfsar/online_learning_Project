
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= 'home' ),
    path('register/', views.register, name='register'),
    path('course_category/', views.course_category, name='course_category'),
    path('courses/<str:foo>/', views.course_detail, name='course_detail'),
    path('letchur/<int:pk>/', views.lecture_detail, name='video'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    
]
