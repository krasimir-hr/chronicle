from django.contrib import admin

from chronicled.games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')