from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.core.cache import cache

from chronicled.common.igdb_api import igdb_search

class HomePageView(TemplateView):
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logged_in_user'] = self.request.user
        return context


class SearchListView(ListView):
    template_name = "common/search.html"
    context_object_name = 'games'

    def get_queryset(self):
        search_query = self.request.GET.get('q')
        if search_query:
            igdb_data = igdb_search(search_query)
            queryset = igdb_data
        else:
            queryset = []
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q')
        context['search_query'] = search_query

        games = context['games']
        game_details = []
        for game in games:
            id = game.get('id', '')
            name = game.get('name', '')
            release_year = game.get('first_release_date', '').year
            summary = game.get('summary', '')
            platforms = game.get('platforms', [])
            cover_id = game.get('cover_id', '')
            slug = game.get('slug', '')

            game_details.append({
                'id': id,
                'name': name,
                'release_year': release_year,
                'summary': summary,
                'platforms': platforms,
                'cover_id': cover_id,
                'slug': slug,
            })
        
        context['game_details'] = game_details

        return context
    
    

    