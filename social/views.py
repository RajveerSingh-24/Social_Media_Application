from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Follow

User = get_user_model()


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def unfollow_user(request, user_id):
    Follow.objects.filter(
        follower=request.user,
        following_id=user_id
    ).delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def feed(request):
    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list('following', flat=True)

    # TODO: Add Post model and uncomment
    # posts = Post.objects.filter(
    #     user__id__in=following_ids
    # ).order_by('-created_at')
    posts = []

    return render(request, 'social/feed.html', {
        'posts': posts,
        'following_ids': following_ids,
    })


@login_required
def search_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query)
    ) if query else []

    return render(request, 'social/search.html', {
        'users': users,
        'query': query
    })

