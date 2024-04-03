from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from .forms import RegistrationForm, LoginForm, ProfileEditForm
from chronicled.common.models import Log
from .models import Profile, AppUser


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


class ProfileDetailsView(DetailView):
    model = AppUser
    template_name = "profiles/profile-details.html"
    context_object_name = "user"
    slug_field = "username"

    def get_object(self, queryset=None):
        username = self.kwargs.get(self.slug_url_kwarg)
        try:
            return self.get_queryset().get(username=username)
        except AppUser.DoesNotExist:
            raise Http404("User does not exist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        user_logs = Log.objects.filter(user=user)
        context['user_logs'] = user_logs
        return context
    
    

class EditProfileView(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "profiles/profile-edit.html"

    def get_object(self, queryset=None):
        return self.request.user.profile


class DeleteProfileView(DeleteView):
    pass