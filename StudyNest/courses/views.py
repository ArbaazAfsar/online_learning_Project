from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lecture, CourseCategory, Enrollment
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, CourseForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User

def home(request):
    return render(request, 'courses/home.html')

@never_cache
@login_required(login_url='/login/')
def course_category(request):
    categories = CourseCategory.objects.all()
    return render(request, 'courses/CourseCategory.html', {'categories': categories})

@never_cache
@login_required(login_url='/login/')
def course_detail(request, foo):
    foo = foo.replace('-', ' ')
    category_obj = get_object_or_404(CourseCategory, name=foo)
    courses = Course.objects.filter(category=category_obj)
    enrolled_courses = {course.id: Enrollment.objects.filter(user=request.user, course=course).exists() for course in courses}
    
    return render(request, 'courses/courses.html', {'courses': courses, 'category_obj': category_obj, 'enrolled_courses': enrolled_courses})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    # Check if the user is already enrolled
    if not Enrollment.objects.filter(user=user, course=course).exists():
        Enrollment.objects.create(user=user, course=course)
        messages.success(request, f'You have been enrolled in {course.title}.')
    else:
        messages.info(request, f'You are already enrolled in {course.title}.')

    return redirect('course_detail', foo=course.category.name)

@login_required(login_url='/login/')
def enrolled_courses(request):
    # Get all courses the user is enrolled in
    enrollments = Enrollment.objects.filter(user=request.user)
    courses = [enrollment.course for enrollment in enrollments]
    
    return render(request, 'courses/enrolled_courses.html', {'courses': courses})



@never_cache
@login_required(login_url='/login/')
def lecture_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lectures = Lecture.objects.filter(course=course)
    
    if not lectures.exists():
        messages.info(request, 'No lectures available for this course.')
        return redirect('course_detail', foo=course.category.name)
    
    return render(request, 'courses/lecture_detail.html', {'lectures': lectures, 'course': course})

@never_cache
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            return redirect('home')  # Redirect to home page or any other page
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'courses/register.html', {'form': form})

@never_cache
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'courses/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    
    return render(request, 'courses/login.html', {'form': form})

@never_cache
def user_logout(request):
    logout(request)
    return redirect('home')



@login_required
def upload_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('my_courses',)
    else:
        form = CourseForm()
    return render(request, 'courses/upload_course.html', {'form': form})


@login_required
def my_courses(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'courses/my_courses.html', {'courses': courses})


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('my_courses')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('my_courses')
    return render(request, 'courses/delete_course_confirm.html', {'course': course})