from django.urls import path
from . import views

urlpatterns = [
    path('superuser/manage-courses/', views.manage_courses, name='manage_courses'),
    path('superuser/upload-category/', views.upload_category, name='upload_category'),
    path('superuser/manage-users/', views.manage_users, name='manage_users'),
    path('superuser/<int:user_id>/ban-user/', views.ban_user, name='ban_user'),
    path('superuser/unban-user/<int:user_id>/', views.unban_user, name='unban_user'),
    path('upload/course/', views.upload_course, name='upload_course'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    
]
