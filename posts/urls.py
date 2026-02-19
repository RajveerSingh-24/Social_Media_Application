from django.urls import path
from .views import create_post
from . import views

urlpatterns = [
    path("", views.home_feed, name="home-feed"),
    path("create/", create_post, name="create-post"),
    path("<int:post_id>/", views.post_detail, name="post-detail"),
    path("<int:post_id>/like/", views.toggle_like, name="toggle-like"),
    path("<int:post_id>/comment/", views.add_comment, name="add-comment"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),

]
