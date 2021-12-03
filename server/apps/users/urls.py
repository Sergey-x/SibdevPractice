from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('me/', views.CustomUserInfoView.as_view(), name='get_user'),
    path('', views.CustomUserCreateView.as_view(), name='create_user'),
]
