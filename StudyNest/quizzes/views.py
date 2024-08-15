from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, StudentQuizAttempt
from .forms import QuizAttemptForm,QuizForm
from courses.models import Course
from django.contrib.auth.decorators import user_passes_test

@login_required
def quiz_detail(request, course_id, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, course__id=course_id)
    
    if request.method == 'POST':
        form = QuizAttemptForm(request.POST, questions=quiz.questions.all())
        if form.is_valid():
            score = 0
            total_marks = 0
            for question in quiz.questions.all():
                selected_choice_id = form.cleaned_data.get(f'question_{question.id}')
                selected_choice = question.choices.get(id=selected_choice_id)
                if selected_choice.is_correct:
                    score += question.marks
                total_marks += question.marks
            
            passed = score >= quiz.passing_marks
            StudentQuizAttempt.objects.create(student=request.user, quiz=quiz, score=score, passed=passed)
            
            return redirect('quiz_result', course_id=course_id, quiz_id=quiz.id)
    else:
        form = QuizAttemptForm(questions=quiz.questions.all())
    
    return render(request, 'quiz_detail.html', {'quiz': quiz, 'form': form})

@login_required
def quiz_result(request, course_id, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    # Get all attempts by the current user for this quiz
    attempts = StudentQuizAttempt.objects.filter(student=request.user, quiz=quiz)

    if attempts.exists():
        attempt = attempts.latest('created_at')  # Now using the newly added field
    else:
        attempt = None

    return render(request, 'quiz_result.html', {
        'quiz': quiz,
        'attempt': attempt,
    })
    
    

def retry_quiz(request, course_id, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, course_id=course_id)
    # Logic to handle retrying the quiz
    return redirect('quiz_detail', course_id=course_id, quiz_id=quiz_id)


def superuser_required(view_func):
    """Decorator to ensure only superusers can access the view."""
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

@superuser_required
def upload_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            return redirect('quiz_detail', pk=quiz.pk)
    else:
        form = QuizForm()
    return render(request, 'upload_quiz.html', {'form': form})

@superuser_required
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, course__instructor=request.user)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('my_courses')
    else:
        form = QuizForm(instance=quiz)
    
    return render(request, 'quizzes/edit_quiz.html', {'form': form, 'quiz': quiz})

@superuser_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, course__instructor=request.user)
    if request.method == 'POST':
        quiz.delete()
        return redirect('my_courses')
    return render(request, 'quizzes/delete_quiz_confirm.html', {'quiz': quiz})