from django.urls import path, include
from chronicled.games import views


urlpatterns = [
    path('<str:slug>/', views.GameDetailView.as_view(), name='game-detail')
]
