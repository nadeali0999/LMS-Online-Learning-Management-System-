from django.urls import path

from apps.payments.views import Free_enrollment, payment_course

urlpatterns = [

    path('enroll/<slug:slug>/', Free_enrollment, name='Enrollment'),
    path('course/<slug:slug>/payment/', payment_course, name='payment_course'),

]
