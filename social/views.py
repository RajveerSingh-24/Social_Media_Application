from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Follow

User = get_user_model()


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if request.user != user_to_follow:
        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

    # redirect to feed (safe, always exists)
    return redirect('feed')


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)

    Follow.objects.filter(
        follower=request.user,
        following=user_to_unfollow
    ).delete()

    # redirect to feed
    return redirect('feed')


@login_required
def feed(request):
    following_users = Follow.objects.filter(
        follower=request.user
    ).select_related('following')

    return render(request, 'social/feed.html', {
        'following_users': following_users
    })