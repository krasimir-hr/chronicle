from django.contrib import admin

from chronicled.common.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_posted')
    list_select_related = ('game',)
