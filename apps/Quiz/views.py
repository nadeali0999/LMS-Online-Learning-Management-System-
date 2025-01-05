from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .forms import QuizForm
from .models import Course, Quiz, QuizAttempt, UserAnswer


@login_required
def quiz_start(request, course_slug, quiz_id):
    course = get_object_or_404(Course, slug=course_slug)
    quiz = get_object_or_404(Quiz, id=quiz_id, course=course)

    context = {'course': course, 'quiz': quiz, }
    return render(request, 'Quiz/quiz_startpage.html', context)


@login_required
def quiz_detail(request, course_slug, quiz_id):
    course = get_object_or_404(Course, slug=course_slug)
    quiz = get_object_or_404(Quiz, id=quiz_id)
    total_time_minutes = quiz.total_time  # Fetching total time from the Quiz model in minutes

    # Convert total_time_minutes to seconds for timer function
    total_time_seconds = total_time_minutes * 60

    if request.method == 'POST':
        form = QuizForm(request.POST, quiz=quiz)
        if form.is_valid():
            quiz_attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz)
            score = 0
            for question in quiz.questions.all():
                selected_option = form.cleaned_data.get(f'question_{question.id}')
                UserAnswer.objects.create(quiz_attempt=quiz_attempt, question=question, selected_option=selected_option)
                if selected_option == question.correct_answer:
                    score += 1
            quiz_attempt.score = score
            quiz_attempt.save()
            total_questions = quiz_attempt.quiz.questions.count()
            percentage = (score / total_questions) * 100
            incorrect_answers = total_questions - score
            print(quiz_attempt)
            return render(request, 'Quiz/quiz_result.html', {'quiz_attempt': quiz_attempt, 'percentage': percentage,
                                                             'incorrect_answers': incorrect_answers, 'score': score})
    else:
        form = QuizForm(quiz=quiz)
        print("inelse")
    return render(request, 'Quiz/quiz_detail.html',
                  {'quiz': quiz, 'form': form, 'total_time_seconds': total_time_seconds})