from django.urls import path, include
from chronicled.games import views


urlpatterns = [
    path('<int:game_id>/', views.GameDetailView.as_view(), name='game-detail')
]
