from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lecture
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def home(request):
    return render(request, 'courses/home.html',)

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

def lecture_detail(request, course_pk, lecture_pk):
    course = get_object_or_404(Course, pk=course_pk)
    lecture = get_object_or_404(Lecture, pk=lecture_pk, course=course)
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


