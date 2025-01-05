from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

urlpatterns = [

     path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),
          name='password_reset'),
     path('password_reset_done/',
          auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
          name='password_reset_done'),
     path('reset/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
          name='password_reset_confirm'),
     path('reset/done/',
          auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
          name='password_reset_complete'),
     path('login/', loginView.as_view(), name='login'),
     path('signup/', signupView.as_view(), name='signup'),
     path('', homeView.as_view(), name='home'),
     path('base', BaseView.as_view(), name='base'),
     path('aboutus/', about_usView.as_view(), name='about_us'),
     path('contact_us/', contact_usView.as_view(), name='contact_us'),
     path('404/', errorView.as_view(), name='404'),
     path('contact/', ContactView.as_view(), name='contact'),
     path('contact/success/', TemplateView.as_view(template_name="main/contact_success.html"), name='contact_success'),
     path('Profile_Update/', Profile_Update, name='Profile_Update'),
     path('logout/', logout_view, name='logout'),

]
