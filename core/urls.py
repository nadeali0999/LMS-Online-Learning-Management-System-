
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('payments/', include('apps.payments.urls')),
    path('courses/', include('apps.courses.urls')),
    path('Quiz/', include('apps.Quiz.urls')),
    path("chat/", include("apps.chat.urls")),
    path('instructor/', include('apps.instructor.urls')),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



