from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, get_object_or_404
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


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "profiles/login.html"

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if remember_me:
            self.request.session.set_expiry(604800)
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    pass


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = "profiles/profile-details.html"
    context_object_name = 'user'
    slug_field = 'slug'

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        try:
            return self.get_queryset().get(slug=slug)
        except AppUser.DoesNotExist:
            raise Http404("User does not exist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        user_logs = Log.objects.filter(user=user)
        context['user_logs'] = user_logs
        return context
    

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'profiles/profile-edit.html'
    slug_field = 'slug'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        user = get_object_or_404(AppUser, slug=slug)
        profile = get_object_or_404(Profile, user=user)
        if self.request.user == user or self.request.user.is_staff:
            return profile
        else:
            raise PermissionDenied("You don't have permission to access this object.")
    
    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        slug = self.request.user.slug
        return reverse_lazy('profile-details', kwargs={'slug': slug})


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = UserModel
    template_name = 'profiles/profile-delete.html'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        user = get_object_or_404(AppUser, slug=slug)
        profile = get_object_or_404(Profile, user=user)
        if self.request.user == user or self.request.user.is_superuser:
            return profile
        else:
            raise PermissionDenied("You don't have permission to access this object.")