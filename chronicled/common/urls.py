from django.urls import path, include
from chronicled.common import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home-page'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('log/<str:slug>/', include([
        path('add/', views.AddGameLogView.as_view(), name='add-log'),
        path('<int:pk>/', views.LogDetailsView.as_view(), name='log-details')
    ]))
]