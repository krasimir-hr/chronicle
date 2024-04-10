from django.urls import path, include
from chronicled.profiles import views


urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('<slug:slug>/', include([
        path('', views.ProfileDetailsView.as_view(), name='profile-details'),
        path('edit/', views.EditProfileView.as_view(), name='profile-edit'),
        path('delete/', views.DeleteProfileView.as_view(), name='profile-delete'),
        ]))
]
