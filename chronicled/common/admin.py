from django.contrib import admin

from chronicled.common.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    pass
