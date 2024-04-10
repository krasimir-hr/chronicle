from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, AppUser

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class AppUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'id', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    inlines = (ProfileInline,)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.is_staff and not request.user.is_superuser:
            # If the user is staff and not a superuser, restrict access
            return False
        return super().has_change_permission(request, obj)


admin.site.register(AppUser, AppUserAdmin)



