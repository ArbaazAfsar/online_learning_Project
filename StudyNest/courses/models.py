from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.core.validators import EmailValidator
from django.core.validators import FileExtensionValidator


class CourseCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    course_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='Categories', null=True, blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='courses', null=True, blank=True)
    description = models.TextField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to='lectures/videos/', blank=True, null=True, validators=[FileExtensionValidator(['mp4', 'mov', 'avi'])])
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def has_video(self):
        return bool(self.video_url or self.video_file)

    def __str__(self):
        return self.title
    
    
    
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} enrolled in {self.course}"
    
    





