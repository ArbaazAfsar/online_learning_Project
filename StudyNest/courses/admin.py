from django.contrib import admin
from .models import Course,CourseCategory,CustomUser

admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(CustomUser)

