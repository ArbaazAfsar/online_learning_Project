from django.contrib import admin
from .models import Course, CourseCategory, Lecture

# Inline class for Lecture
class LectureInline(admin.TabularInline):
    model = Lecture
    extra = 1  # Number of empty lecture fields to display by default
    can_delete = True
    fields = ('title', 'video_url', 'video_file', 'order')

# Admin class for Course
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'created_at', 'video_count')
    search_fields = ('title', 'instructor__username', 'category__name')
    list_filter = ('category', 'instructor', 'created_at')
    inlines = [LectureInline]  # Include lectures inline within the course

# Admin class for CourseCategory
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_count')
    search_fields = ('name',)
    list_filter = ('name',)

# Registering models with the admin site
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)