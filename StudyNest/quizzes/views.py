from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question
# Create your views here.


def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        score = 0
        for question in quiz.questions.all():
            selected_answer = request.POST.get(f'question-{question.id}')
            if selected_answer:
                correct_answer = question.answers.filter(is_correct=True).first()
                if selected_answer == str(correct_answer.id):
                    score += 1
        return render(request, 'quiz/result.html', {'quiz': quiz, 'score': score, 'total': quiz.questions.count()})
    
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})