from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.db import models


from chronicled.profiles.validators import validate_file_size
from chronicled.profiles.managers import AppUserManager

class AppUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        unique=True,
        null=False,
        blank=False,
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    objects = AppUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


UserModel = get_user_model()

class Profile(models.Model):
    NAME_MAX_SIZE = 30

    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=NAME_MAX_SIZE,
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=NAME_MAX_SIZE,
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    profile_picture = models.ImageField(
        null=True,
        blank=True,
        validators=(validate_file_size,),
        upload_to='images/profile-pictures'
    )



