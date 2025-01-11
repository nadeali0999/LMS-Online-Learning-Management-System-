from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, FormView

from apps.courses.models import Categories, Course
from .forms import ContactForm
from .forms import loginForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

class BaseView(TemplateView):
    template_name = 'base.html'


class ContactView(FormView):
    template_name = 'main/contact_us.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class errorView(TemplateView):
    template_name = '404_Error/404.html'

    def get_context_data(self, **kwargs):
        # First, call the base implementation to get a context
        context = super().get_context_data(**kwargs)
        # Add custom context data, here assuming Categories is properly imported and get_all_categories is a valid method
        context['categories'] = Categories.get_all_categories()
        return context


class signupView(TemplateView):
    template_name = 'accounts/signup.html'

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check email
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists!')
            return redirect('signup')

        # Check username
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists!')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')

    def get(self, request):
        return render(request, self.template_name)


class loginView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = loginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = loginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Assuming you're using email as the username
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Email and password are invalid!')
            except User.DoesNotExist:
                messages.error(request, 'Email and password are invalid!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}: {}".format(field, error))
        return render(request, self.template_name, {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

class homeView(TemplateView):
    template_name = 'main/home.html'  # Ensure you specify your template

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the queryset of categories, ordered by 'id' and limited to the first 5
        context['categories'] = Categories.objects.all().order_by('id')[:5]
        context['course'] = Course.objects.filter(status='PUBLISH').order_by('-id')

        return context


class about_usView(TemplateView):
    template_name = 'main/about_us.html'

    def get_context_data(self, **kwargs):
        # First, call the base implementation to get a context
        context = super().get_context_data(**kwargs)
        # Add custom context data, here assuming Categories is properly imported and get_all_categories is a valid method
        context['categories'] = Categories.get_all_categories()
        return context


class contact_usView(TemplateView):
    template_name = 'main/contact_us.html'

    def get_context_data(self, **kwargs):
        # First, call the base implementation to get a context
        context = super().get_context_data(**kwargs)
        # Add custom context data, here assuming Categories is properly imported and get_all_categories is a valid method
        context['categories'] = Categories.get_all_categories()
        return context


@login_required
def Profile_Update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)

        # Check if the new username is different from the current one and if it already exists
        if username != user.username and User.objects.filter(username=username).exists():
            # Handle the case where the username already exists
            # You can display an error message or take appropriate action
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect('Profile_Update')

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)  # Re-authenticate the user
            messages.success(request, 'Profile and password successfully updated.')
        else:
            user.save()
            messages.success(request, 'Profile successfully updated.')

        return redirect('home')
    else:
        user = request.user
        context = {
            'user': user,
        }
        return render(request, 'accounts/profile.html', context)
