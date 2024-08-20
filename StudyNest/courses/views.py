from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lecture, CourseCategory, Enrollment
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, CourseForm, CategoryForm,LectureForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

def home(request):
    # Fetch all categories and their related courses
    categories = CourseCategory.objects.prefetch_related('courses').all()

    # Pass the data to the template
    return render(request, 'courses/home.html', {'categories': categories})

@never_cache
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

@login_required(login_url='/login/')
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

def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment = Enrollment.objects.filter(course=course, user=request.user).first()
    
    if enrollment:
        enrollment.delete()
    
    return redirect('enrolled_courses')

def course_quizzes(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    quizzes = course.quizzes.all()  # Assuming 'quizzes' is a related name for quizzes in the Course model
    return render(request, 'courses/course_quizzes.html', {'course': course, 'quizzes': quizzes})

@never_cache
@login_required(login_url='/login/')
def lecture_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lectures = Lecture.objects.filter(course=course)
    
    if not lectures.exists():
        messages.info(request, 'No lectures available for this course.')
        # return redirect('course_detail', foo=course.category.name)
    
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
            messages.success(request, ('you have been logged in.....'))
            return redirect('home')
        else:
            return render(request, 'courses/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    
    return render(request, 'courses/login.html', {'form': form})

@never_cache
def user_logout(request):
    logout(request)
    messages.success(request,("you have been logged out....."))
    return redirect('home')

@never_cache
@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_lectures(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.course = course
            lecture.save()
            return redirect('lecture_detail', pk=course_id)
    else:
        form = LectureForm()

    lectures = Lecture.objects.filter(course=course)
    return render(request, 'courses/manage_lectures.html', {'course': course, 'lectures': lectures, 'form': form})


@login_required
def edit_lecture(request, lecture_id):
    # Fetch the lecture object
    lecture = get_object_or_404(Lecture, id=lecture_id)
    
    if request.method == 'POST':
        # Instantiate the form with POST data and any uploaded files
        form = LectureForm(request.POST, request.FILES, instance=lecture)
        if form.is_valid():
            form.save()
            return redirect('lecture_detail', pk=lecture.course.id)
    else:
        # Instantiate the form with the lecture instance for GET requests
        form = LectureForm(instance=lecture)
    
    return render(request, 'courses/edit_lecture.html', {'form': form, 'lecture': lecture})


@login_required
def delete_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    if request.method == 'POST':
        course_id = lecture.course.id
        lecture.delete()
        return redirect('lecture_detail', pk=course_id)
    return render(request, 'courses/confirm_delete.html', {'lecture': lecture})


def about(request):
    return render(request, 'courses/about.html')

def contact(request):
    return render(request, 'courses/contact.html')









