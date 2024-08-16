from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from courses.forms import CategoryForm,CourseForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from courses.models import Course
from django.contrib.auth.decorators import login_required

# Create your views here.


#-------Superuser section-------



def superuser_required(view_func):
    """Decorator to ensure only superusers can access the view."""
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

@never_cache
@superuser_required
def manage_courses(request):
    courses = Course.objects.all()
    return render(request, 'manage_courses.html', {'courses': courses})

@never_cache
@superuser_required
def manage_users(request):
    superusers = User.objects.filter(is_superuser=True)
    regular_users = User.objects.filter(is_superuser=False)
    
    print("Superusers: ", list(superusers))
    print("Regular Users: ", list(regular_users))
    
    
    return render(request, 'manage_user.html', {
        'superusers': superusers,
        'regular_users': regular_users
    })

@never_cache
@superuser_required
def ban_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        messages.success(request, f'User {user.username} has been banned.')
        return redirect('manage_users')
    return render(request, 'ban_user_confirm.html', {'user': user})

@never_cache
@superuser_required
def unban_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = True
        user.save()
        messages.success(request, f'User {user.username} has been unbanned.')
        return redirect('manage_users')
    return render(request, 'unban_user_confirm.html', {'user': user})

@never_cache
@superuser_required
def upload_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category uploaded successfully.')
            return redirect('upload_category')
    else:
        form = CategoryForm()

    return render(request, 'upload_category.html', {'form': form})


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('manage_courses')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'edit_course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('manage_courses')
    return render(request, 'delete_course_confirm.html', {'course': course})


@login_required
def upload_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('manage_courses',)
    else:
        form = CourseForm()
    return render(request, 'upload_course.html', {'form': form})