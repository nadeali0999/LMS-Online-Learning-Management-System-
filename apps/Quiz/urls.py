# quizzes/urls.py

from django.urls import path
from . import views
from .views import quiz_detail

urlpatterns = [
    path('course/<slug:course_slug>/quiz/<int:quiz_id>/', views.quiz_start, name='quiz_start'),
    path('course/<slug:course_slug>/quiz/<int:quiz_id>/details/', views.quiz_detail, name='quiz_details'),

]
