from django.urls import path
from .views import public_profile_view

urlpatterns = [
    path('<str:username>/', public_profile_view, name='user-profile'),
]
