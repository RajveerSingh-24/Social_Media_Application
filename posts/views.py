from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostCreateForm
from django.shortcuts import render, get_object_or_404
from .models import Post
from .models import Like
from .models import Comment
from .forms import CommentForm
from users.models import Follow
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse

@login_required
def create_post(request):

    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # redirect to profile after posting
            return redirect("user-profile", username=request.user.username)

    else:
        form = PostCreateForm()

    return render(request, "posts/create_post.html", {
        "form": form
    })

@login_required
def post_detail(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    post.is_liked = Like.objects.filter(
        user=request.user,
        post=post
    ).exists()

    comments = post.comments.select_related("user")

    form = CommentForm()

    return render(request, "posts/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form
    })



    
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    # If already existed → unlike
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    likes_count = Like.objects.filter(post=post).count()

    return JsonResponse({
        "liked": liked,
        "likes_count": likes_count
    })


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

    return redirect("post-detail", post_id=post.id)

@login_required
def home_feed(request):

    posts = Post.objects.all().select_related("user")

    for post in posts:
        post.is_liked = Like.objects.filter(
            user=request.user,
            post=post
        ).exists()

    return render(request, "posts/home_feed.html", {
        "posts": posts
    })


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Security: only owner can delete
    if post.user != request.user:
        messages.error(request, "You cannot delete this post.")
        return redirect("public_profile", username=post.user.username)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect("public_profile", username=request.user.username)

    # fallback safety
    return redirect("public_profile", username=post.user.username)

@login_required
def add_comment(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

    return redirect("post-detail", post_id=post.id)