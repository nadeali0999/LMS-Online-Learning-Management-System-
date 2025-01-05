from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from apps.courses import views
from apps.courses.views import *

urlpatterns = [
    path('single_course/', SingleCourseView.as_view(), name='single_course'),
    path('course/filter-data',views.filter_data,name="filter-data"),
    path('search/', SearchCourseView.as_view(), name='search_course'),
    path('course/<slug:slug>',course_detailsView.as_view(), name='course_details'),
    path('watch_course/<slug:slug>/', watch_course, name='watch_course'),
    path('my_learning/', my_learning, name='my_learning'),


]
