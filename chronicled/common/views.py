from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.views.generic.edit import FormMixin, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count, Avg
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

from chronicled.common.igdb_api import igdb_search, fetch_game_by_slug
from chronicled.common.models import Log, Comment, Like, CommentLike
from chronicled.common.forms import LogForm, CommentForm
from chronicled.games.models import Game

UserModel = get_user_model()


class HomePageView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return AuthenticatedHomeView.as_view()(request, *args, **kwargs)
        else:
            return NonAuthenticatedHomeView.as_view()(request, *args, **kwargs)


class AuthenticatedHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logged_in_user'] = self.request.user

        def get_trending_games():
            last_week = datetime.now() - timedelta(weeks=1)
            start_date = last_week - timedelta(days=last_week.weekday())

            trending_games = (Game.objects
                              .filter(logs__date_posted__gte=start_date)
                              .annotate(total_logs=Count('logs'))
                              .order_by('-total_logs'))[:6]

            return trending_games

        def get_highest_rated_games():
            highest_rated_games = (Game.objects
                                   .annotate(avg_rating=Avg('logs__rating'))
                                   .exclude(logs__rating=None)
                                   .order_by('-avg_rating'))[:6]

            return highest_rated_games

        def get_latest_reviews():
            latest_reviews = (Log.objects
                              .exclude(review_text__exact="")
                              .order_by('-date_posted'))[:4]
            return latest_reviews

        def get_welcome_name():
            welcome_name = ""
            user = self.request.user
            if user.profile.first_name:
                welcome_name = user.profile.first_name
            else:
                welcome_name = user.username
            return welcome_name

        context['trending_games'] = get_trending_games()
        context['highest_rated_games'] = get_highest_rated_games()
        context['latest_reviews'] = get_latest_reviews()
        context['welcome_name'] = get_welcome_name()

        return context


class NonAuthenticatedHomeView(TemplateView):
    template_name = 'common/landing-page.html'


class SearchListView(LoginRequiredMixin, ListView):
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


class BaseLogView(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug')
        self.game_data = fetch_game_by_slug(self.slug)
        self.name = self.game_data[0]['name']
        self.cover_id = self.game_data[0]['cover']['image_id']
        self.platforms = [(platform['id'], platform['name']) for platform in self.game_data[0]['platforms']]
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['platform_choices'] = self.platforms
        return kwargs

    def form_valid(self, form):
        game_db, created = Game.objects.get_or_create(slug=self.slug)
        if created:
            game_db.slug = self.slug
            game_db.name = self.name
            game_db.cover_id = self.cover_id
            game_db.save()

        form.instance.game = game_db
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.game_data[0]['name']
        context['cover_id'] = self.game_data[0]['cover']['image_id']
        return context

    def get_success_url(self):
        return reverse_lazy('game-detail', kwargs={'slug': self.slug})


class CreateLogView(BaseLogView, CreateView):
    model = Log
    form_class = LogForm
    template_name = 'common/log-create.html'
    context_object_name = 'log'


class EditLogView(BaseLogView, UpdateView):
    model = Log
    form_class = LogForm
    template_name = 'common/log-edit.html'
    context_object_name = 'log'


class DeleteLogView(DeleteView):
    model = Log
    template_name = 'common/log-delete.html'
    success_url = reverse_lazy('home-page')
    context_object_name = 'log'


class LogDetailsView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'common/log-details.html'
    model = Log
    context_object_name = 'log'
    form_class = CommentForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm
        context["comments"] = Comment.objects.filter(to_log=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.to_log = self.get_object()
        comment.user = self.request.user
        comment.date_time_posted = datetime.now()
        comment.save()
        return redirect(self.get_success_url())


class LikeFunctionalityView(View):
    def get(self, request, log_id):
        log = Log.objects.get(id=log_id)
        liked_object = Like.objects.filter(to_log_id=log_id, user=request.user).first()

        if liked_object:
            liked_object.delete()
        else:
            like = Like(to_log=log, user=request.user)
            like.save()

        referer = request.META.get('HTTP_REFERER')
        return redirect(referer + f'#{log_id}')


class CommentLikeFunctionalityView(View):
    def get(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        liked_object = CommentLike.objects.filter(to_comment_id=comment_id, user=request.user).first()

        if liked_object:
            liked_object.delete()
        else:
            like = CommentLike(to_comment=comment, user=request.user)
            like.save()

        referer = request.META.get('HTTP_REFERER')
        return redirect(referer + f'#{comment_id}')