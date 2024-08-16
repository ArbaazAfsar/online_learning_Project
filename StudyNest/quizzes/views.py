from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, StudentQuizAttempt
from .forms import QuizAttemptForm,QuizForm, Question, QuestionForm, Quiz, ChoiceFormSet ,ChoiceForm, Choice
from courses.models import Course
from django.contrib.auth.decorators import user_passes_test
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
import random


@login_required
def quiz_detail(request, course_id, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, course__id=course_id)
    
    # Get all questions related to the quiz
    questions = list(quiz.questions.all())
    
    # Randomly select 10 questions
    random_questions = random.sample(questions, 10) if len(questions) >= 10 else questions
    
    if request.method == 'POST':
        form = QuizAttemptForm(request.POST, questions=random_questions)
        if form.is_valid():
            score = 0
            total_marks = 0
            for question in random_questions:
                selected_choice_id = form.cleaned_data.get(f'question_{question.id}')
                selected_choice = question.choices.filter(id=selected_choice_id).first()
                if selected_choice and selected_choice.is_correct:
                    score += question.marks
                total_marks += question.marks
            
            passed = score >= quiz.passing_marks
            StudentQuizAttempt.objects.create(student=request.user, quiz=quiz, score=score, passed=passed)
            
            return redirect('quiz_result', course_id=course_id, quiz_id=quiz.id)
    else:
        form = QuizAttemptForm(questions=random_questions)
    
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

QuestionFormSet = inlineformset_factory(Quiz, Question, form= QuestionForm, extra=1)

@superuser_required
def upload_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix='questions')
        choice_formsets = [ChoiceFormSet(request.POST, prefix=f'choices_{i}') for i in range(20)]
        
        if quiz_form.is_valid() and question_formset.is_valid() and all(cf.is_valid() for cf in choice_formsets):
            quiz = quiz_form.save()
            questions = question_formset.save(commit=False)
            for i, question in enumerate(questions):
                question.quiz = quiz
                question.save()
                choices = choice_formsets[i].save(commit=False)
                for choice in choices:
                    choice.question = question
                    choice.save()
            
            return redirect('success_view_name')  # Replace with your actual success view name
    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet(prefix='questions')
        choice_formsets = [ChoiceFormSet(prefix=f'choices_{i}') for i in range(20)]
    
    return render(request, 'upload_quiz.html', {
        'quiz_form': quiz_form,
        'question_formset': question_formset,
        'choice_formsets': choice_formsets,
    })
    
def success_view(request):
    return render(request, 'success.html')
    
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
    
    return render(request, 'edit_quiz.html', {'form': form, 'quiz': quiz})

@superuser_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, course__instructor=request.user)
    if request.method == 'POST':
        quiz.delete()
        return redirect('my_courses')
    return render(request, 'delete_quiz_confirm.html', {'quiz': quiz})