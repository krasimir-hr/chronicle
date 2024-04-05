from django.urls import path, include
from chronicled.common import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home-page'),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('like/<int:log_id>/', views.LikeFunctionalityView.as_view(), name='like'),
    path('comment-like/<int:comment_id>/', views.CommentLikeFunctionalityView.as_view(), name='comment-like'),
    path('log/<str:slug>/', include([
        path('add/', views.CreateLogView.as_view(), name='add-log'),
        path('<int:pk>/', include([
            path('', views.LogDetailsView.as_view(), name='log-details'),
            path('edit/', views.EditLogView.as_view(), name='log-edit'),
            path('delete/', views.DeleteLogView.as_view(), name='log-delete'),
        ]))
    ]))
]
