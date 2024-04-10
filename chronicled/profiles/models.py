import os.path

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify

from chronicled.profiles.validators import validate_file_size, validate_no_spaces
from chronicled.profiles.managers import AppUserManager


class AppUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        validators=[validate_no_spaces, MinLengthValidator(5)],
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

    slug = models.SlugField(unique=True, blank=True)

    objects = AppUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


UserModel = get_user_model()


def profile_picture_path(instance, filename):
    username = instance.user.username
    _, ext = os.path.splitext(filename)
    return f'profile-pictures/{username}-profile-pic{ext}'


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
        upload_to=profile_picture_path,
        default='images/anon-user.webp',
    )


