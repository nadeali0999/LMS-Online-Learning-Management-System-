from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Course, Video
from apps.courses.models import *
from apps.payments.models import Enrollment
from ..Quiz.models import QuizAttempt, Quiz

from django.shortcuts import redirect
from django.views.generic import TemplateView


class SingleCourseView(TemplateView):
    template_name = 'main/single_course.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['FreeCourse_count'] = Course.objects.filter(price=0).count()
        context['PaidCourse_count'] = Course.objects.filter(price__gte=1).count()
        context['levels'] = Level.objects.all()
        context['course'] = Course.objects.all()
        context['categories'] = Categories.get_all_categories()  # Ensuring correct method call
        return context


class SearchCourseView(ListView):
    model = Course
    template_name = 'search/search.html'
    context_object_name = 'course'

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Course.objects.filter(title__icontains=query)



class course_detailsView(TemplateView):
    template_name = 'courses/course_details.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            self.course = Course.objects.get(slug=slug)
        except Course.DoesNotExist:
            # Redirect to the custom 404 page
            return redirect('404')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course

        # Calculate the total duration of videos related to the course
        total_duration = Video.objects.filter(course=self.course).aggregate(total=Sum('time_duration'))['total']
        context['time_duration'] = total_duration

        user = self.request.user
        if user.is_authenticated:
            is_enrolled = Enrollment.objects.filter(course=self.course, user=user).exists()
            context['is_enrolled'] = is_enrolled

            # Fetch the user's quiz attempt score for this course
            quizzes = self.course.quizzes.all()
            quiz_attempts = QuizAttempt.objects.filter(user=user, quiz__in=quizzes)
            quiz_score = None

            if quiz_attempts.exists():
                # Assume there's only one quiz per course for simplicity
                quiz_score = quiz_attempts.first().score

            context['quiz_score'] = quiz_score  # Pass the quiz score to the template
        else:
            context['is_enrolled'] = False
            context['quiz_score'] = None

        # Fetch all videos related to the course
        videos = Video.objects.filter(course=self.course)
        context['videos'] = videos

        # Check if all videos are marked as complete
        all_videos_completed = all(video.is_completed for video in videos)
        context['all_videos_completed'] = all_videos_completed

        # Calculate the course count
        course_count = Course.objects.count()
        context['course_count'] = course_count

        # Calculate the number of enrolled students for the course
        enrolled_students_count = Enrollment.objects.filter(course=self.course).count()
        context['enrolled_students_count'] = enrolled_students_count

        return context







@login_required
def watch_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    lectures = course.video_set.all()  # Fetch all videos associated with the course
    time_duration = lectures.aggregate(total=Sum('time_duration'))['total']
    lecture_id = request.GET.get('lecture')

    if lecture_id:
        video = get_object_or_404(Video, id=lecture_id, course=course)
    else:
        # If no specific video is requested, render the first video in the course
        video = course.video_set.first()

    if request.method == 'POST' and 'video_id' in request.POST:
        video_id = request.POST.get('video_id')
        video = get_object_or_404(Video, id=video_id, course=course)
        video.is_completed = True
        video.save()

    # Check if all videos are marked as complete
    all_videos_completed = all(video.is_completed for video in lectures)

    # Fetch the user's quiz attempt score for this course
    quizzes = course.quizzes.all()
    quiz_attempts = QuizAttempt.objects.filter(user=request.user, quiz__in=quizzes)
    quiz_score = None

    if quiz_attempts.exists():
        # Assume there's only one quiz per course for simplicity
        quiz_score = quiz_attempts.first().score

    return render(request, 'courses/watch_course.html', {
        'course': course,
        'time_duration': time_duration,
        'is_enrolled': is_enrolled,
        'video': video,
        'all_videos_completed': all_videos_completed,
        'quiz_score': quiz_score,  # Pass the quiz score to the template
    })


def my_learning(request):
    user = request.user
    enrolled_courses = Course.objects.filter(enrollment__user=user)

    course_data = []
    quizzes = Quiz.objects.filter(course__in=enrolled_courses)
    quiz_attempts = QuizAttempt.objects.filter(user=user, quiz__in=quizzes)

    quiz_scores = {attempt.quiz.course.id: attempt.score for attempt in quiz_attempts}

    for course in enrolled_courses:
        score = quiz_scores.get(course.id, None)
        course_data.append({
            'course': course,
            'quiz_score': score
        })

    return render(request, 'main/my_learning.html', {
        'course_data': course_data,
    })

def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    if price == ['PriceFree']:
        course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
        course = Course.objects.all()
    elif categories:
        course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')

    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t})
