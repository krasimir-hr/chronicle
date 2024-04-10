from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, AppUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


class CustomAppUserAdmin(UserAdmin):
    list_display = ('id', 'username')

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.is_staff and not request.user.is_superuser:
            # If the user is staff and not a superuser, restrict access
            return False
        return super().has_change_permission(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomAppUserAdmin)


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')


