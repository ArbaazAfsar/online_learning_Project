from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from courses.forms import CategoryForm,CourseForm, CategoryForm,ReviewForm,LectureForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from courses.models import Course,Review, Lecture, CourseCategory
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

@never_cache
@superuser_required
def manage_categories(request):
    categories = CourseCategory.objects.all()
    return render(request, 'manage_categories.html', {'categories': categories})

def edit_category(request, category_id):
    category = get_object_or_404(CourseCategory, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form, 'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(CourseCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('manage_categories')
    return render(request, 'delete_category_confirm.html', {'category': category})

@never_cache
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
@never_cache
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('manage_courses')
    return render(request, 'delete_course_confirm.html', {'course': course})

@never_cache
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
    return render(request, 'manage_lectures.html', {'course': course, 'lectures': lectures, 'form': form})


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
    
    return render(request, 'confirm_delete.html', {'form': form, 'lecture': lecture})


@login_required
def delete_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    if request.method == 'POST':
        course_id = lecture.course.id
        lecture.delete()
        return redirect('lecture_detail', pk=course_id)
    return render(request, 'confirm_delete.html', {'lecture': lecture})

def upload_lecture(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = LectureForm(request.POST, request.FILES)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.course = course
            lecture.save()
            messages.success(request, 'Lecture uploaded successfully.')
            return redirect('manage_lectures', course_id=course_id)
    else:
        form = LectureForm()

    return render(request, 'upload_lecture.html', {'form': form, 'course': course})


@login_required
@superuser_required
def review_management(request):
    reviews = Review.objects.all()
    return render(request, 'review_management.html', {'reviews': reviews})

@login_required
@superuser_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('review_management')  # Redirect to the management page after deletion
    return render(request, 'review_confirm_delete.html', {'review': review})