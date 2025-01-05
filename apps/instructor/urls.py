from django.urls import path

from apps.instructor import views

urlpatterns = [
    path('instructor/', views.instructors_list, name='instructor'),
]