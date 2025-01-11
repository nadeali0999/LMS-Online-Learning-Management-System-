import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from apps.courses.models import Course
from apps.payments.models import Enrollment

stripe.api_key = settings.STRIPE_SECRET_KEY


def Free_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    user = request.user

    # Check if the user is already enrolled
    enrollment_exists = Enrollment.objects.filter(user=user, course=course).exists()

    if course.price == 0 and not enrollment_exists:
        # Enroll the user in the free course
        Enrollment.objects.create(user=user, course=course)
        return redirect('home')
    else:
        # Handle cases where the course is not free or the user is already enrolled
        return redirect('course_details', slug=slug)


def payment_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    user = request.user

    # Check if the user is already enrolled
    enrollment_exists = Enrollment.objects.filter(user=user, course=course).exists()

    if enrollment_exists:
        return redirect('course_details', slug=slug)

    if request.method == 'POST':
        token = request.POST['stripeToken']

        try:
            charge = stripe.Charge.create(amount=int(course.price * 100),  # Amount in cents
                currency='usd', description=f'Payment for {course.title}', source=token, )

            Enrollment.objects.create(user=user, course=course, paid=True)
            return redirect('home')

        except stripe.error.StripeError as e:
            return render(request, 'payment/course_payment.html', {'course': course, 'error': str(e),
                'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY, })

    return render(request, 'payment/course_payment.html',
                  {'course': course, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY, })
