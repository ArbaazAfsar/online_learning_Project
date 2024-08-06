from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.core.validators import EmailValidator

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title




class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, validators=[EmailValidator()])


    # Role field
    STUDENT = 'student'
    INSTRUCTOR = 'instructor'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (INSTRUCTOR, 'Instructor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Avoid conflict with auth.User.groups
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Avoid conflict with auth.User.user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email  # Changed to return email as identifier

    # Ensure `email` field is used as a unique identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']