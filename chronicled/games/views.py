from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.http import Http404

from chronicled.common.igdb_api import fetch_game_by_slug, get_companies, get_genres, get_platforms
from chronicled.games.models import Game


class GameDetailView(TemplateView):
    template_name = 'games/game_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        game = fetch_game_by_slug(slug)

        context['name'] = game[0]['name']
        context['release_date'] = game[0]['first_release_date']
        context['cover_id'] = game[0]['cover']['image_id']
        context['summary'] = game[0]['summary']
        context['companies'] = get_companies(game)
        context['genres'] = get_genres(game)
        context['platforms'] = get_platforms(game)
        screenshots = game[0].get('screenshots', [])
        if screenshots:
            context['screenshot'] =  screenshots[0]['image_id']
        else:
            context['screenshot'] = None
        
        return context