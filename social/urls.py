from django.urls import path
from . import views


urlpatterns = [
    path('follow/<str:username>/', views.follow_user, name='follow'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow'),
    path('feed/', views.feed, name='feed'),
]

app_name = "social"