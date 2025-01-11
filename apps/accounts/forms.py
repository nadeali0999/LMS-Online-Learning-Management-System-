from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from apps.accounts.models import Contact


class signUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class loginForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput)



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match("^[a-zA-Z]*$", name):
            raise ValidationError('Name should only contain alphabetic characters.')
        return name

