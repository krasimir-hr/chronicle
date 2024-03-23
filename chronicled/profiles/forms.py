from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from .models import AppUser

UserModel = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'autofocus': True}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    remember_me = forms.BooleanField(
        required=False,
        label='Remember me.'
    )