from django.contrib import admin

from .models import Profile, AppUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

