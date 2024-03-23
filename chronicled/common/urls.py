from django.urls import path, include
from chronicled.common import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home-page'),
    path('search', views.SearchListView.as_view(), name='search')
]
