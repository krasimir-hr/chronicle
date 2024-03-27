from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from chronicled.profiles.forms import RegistrationForm, LoginForm

UserModel = get_user_model()

class RegistrationView(CreateView):
    model = UserModel
    form_class = RegistrationForm
    template_name = "profiles/registration.html"
    success_url = reverse_lazy('login')

class LoginView(LoginView):
    form_class = LoginForm
    template_name = "profiles/login.html"

class LogoutView(LogoutView):
    pass