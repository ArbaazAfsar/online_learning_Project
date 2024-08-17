from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, StudentQuizAttempt
from .forms import QuizAttemptForm,QuizForm, Question, QuestionForm, Quiz, ChoiceFormSet ,ChoiceForm, Choice,QuestionFormSet
from courses.models import Course
from django.contrib.auth.decorators import user_passes_test
from django.forms import inlineformset_factory
from django.forms import modelformset_factory
import random
from django.contrib import messages


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



@superuser_required
# def upload_quiz(request):
#     if request.method == 'POST':
#         quiz_form = QuizForm(request.POST)
#         question_formset = QuestionFormSet(request.POST)
        
#         if quiz_form.is_valid() and question_formset.is_valid():
#             quiz = quiz_form.save()
#             print('aaaaaaa')
            
#             questions = question_formset.save(commit=False)
#             for question in questions:
#                 question.quiz = quiz  # Assign the quiz to each question
#                 question.save()
#                 print('aaaaaaa')
                
#                 # For each question, create its choice formset
#                 choice_formset = ChoiceFormSet(request.POST, instance=question)
#                 if choice_formset.is_valid():
#                     choices = choice_formset.save(commit=False)
#                     for choice in choices:
#                         choice.question = question  # Assign the question to each choice
#                         choice.save()
            
#             return redirect('success_view_name')  # Replace with your actual success view name
#     else:
#         quiz_form = QuizForm()
#         question_formset = QuestionFormSet(queryset=Quiz.objects.none())  # No initial data
#         choice_formsets = ChoiceFormSet()
    
#     return render(request, 'upload_quiz.html', {
#         'quiz_form': quiz_form,
#         'question_formset': question_formset,
#         'choice_formsets': choice_formsets,
#     })
def upload_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            
            choice_formset = ChoiceFormSet(request.POST, instance=question)
            if choice_formset.is_valid():
                choice_formset.save()
                messages.success(request, 'Question and choices uploaded successfully!')
                # Assume that you have a way to get course_id related to the quiz
                course_id = quiz.course.id
                return redirect('quiz_detail', course_id=course_id, quiz_id=quiz.id)
            else:
                messages.error(request, 'There was an error with the choices.')
        else:
            messages.error(request, 'There was an error with the question.')
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet()

    return render(request, 'upload_question.html', {
        'quiz': quiz,
        'question_form': question_form,
        'choice_formset': choice_formset,
    })
    
    
    
@superuser_required
def upload_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        
        if quiz_form.is_valid():
            quiz = quiz_form.save()  # Save and get the single Quiz instance
            messages.success(request, 'Quiz uploaded successfully!')
            return redirect('upload_question', quiz_id=quiz.id)  # Redirect with quiz_id
        else:
            messages.error(request, 'The quiz form is not valid.')
    else:
        quiz_form = QuizForm()  # Initialize the form in GET request

    return render(request, 'upload_quiz.html', {'quiz_form': quiz_form})
        


def quiz_detail_view(request, course_id, quiz_id):
    # Retrieve the quiz object
    quiz = get_object_or_404(Quiz, id=quiz_id, course_id=course_id)
    
    # Fetch all the questions related to this quiz
    questions = quiz.questions.all()

    # Create a form for quiz attempt if it's a POST request
    if request.method == 'POST':
        form = QuizAttemptForm(request.POST, questions=questions)
        if form.is_valid():
            # Process the form and evaluate the quiz
            # (You can add logic to calculate scores, save the attempt, etc.)
            # Redirect to a results page or show the result directly
            return redirect('quiz_result', course_id=course_id, quiz_id=quiz.id)
    else:
        # Initialize the form for a GET request
        form = QuizAttemptForm(questions=questions)
    
    context = {
        'quiz': quiz,
        'form': form,
    }

    return render(request, 'quiz_detail.html', context)


def success_view(request):
    return render(request, 'success.html', {'message': 'Operation completed successfully!'})
    
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