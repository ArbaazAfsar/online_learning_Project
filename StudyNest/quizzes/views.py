from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, StudentQuizAttempt
from .forms import QuizAttemptForm
from courses.models import Course

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
