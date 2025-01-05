from django.db.models import Q
from django.shortcuts import render

from apps.instructor.models import Author


def instructors_list(request):
    query = request.GET.get('q')
    authors = Author.objects.all()

    if query:  # Check if query parameter exists
        authors = authors.filter(
            Q(user__username__icontains=query) |
            Q(profession__icontains=query)
        )

    return render(request, 'instructors/intstructors.html', {'authors': authors})