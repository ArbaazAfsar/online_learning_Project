from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lecture,CourseCategory
from django.contrib.auth import login,logout,authenticate
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'courses/home.html',)

@login_required(login_url='/login/')
def course_category(request):
    Category = CourseCategory.objects.all()
    return render(request, 'courses/CourseCategory.html',{'Category':Category} )


@login_required(login_url='/login/')
def course_detail(request, foo):
    foo = foo.replace('-', ' ')
    category_obj = CourseCategory.objects.get(name=foo )
    courses = Course.objects.filter(category = category_obj)
          
    return render(request, 'courses/courses.html', {'courses': courses, 'category_obj':category_obj})

@login_required(login_url='/login/')
def lecture_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    lecture = Lecture.objects.filter(course = course)
    return render(request, 'courses/lecture_detail.html', {'lecture': lecture, 'course': course})



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a home page or dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'courses/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a home page or dashboard
        
    else:
        form = AuthenticationForm()
    return render(request, 'courses/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to a home page or login page

