from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser,Group,Permission,User
from django.core.validators import EmailValidator
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


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

    def student_count(self):
        return self.enrollments.count()

    def lecture_count(self):
        return self.lecture_set.count()
    

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='lectures/', blank=True, null=True)
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

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
    
    
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()  # Main content of the review
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Rating given by the user # Rating given by the user
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the review was created

    def __str__(self):
        return f"Review by {self.user.username}"
    
    





