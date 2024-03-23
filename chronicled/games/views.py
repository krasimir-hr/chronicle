from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.http import Http404

from chronicled.common.igdb_api import fetch_game_by_id


class GameDetailView(TemplateView):
    template_name = 'games/game_detail.html'

    def get_queryset(self):
        search_query = self.request.GET.get('q')
        if search_query:
            igdb_data = fetch_game_by_id(search_query)
            queryset = igdb_data
        else:
            queryset = []
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game_id = self.kwargs.get('game_id')
        game_data = fetch_game_by_id(game_id)
        context['game_data'] = game_data
        return context