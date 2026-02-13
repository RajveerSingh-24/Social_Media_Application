
# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

@login_required
def conversation(request, username):
    other_user = get_object_or_404(User, username=username)

    messages = Message.objects.filter(
        sender=request.user,
        receiver=other_user
    ) | Message.objects.filter(
        sender=other_user,
        receiver=request.user
    )

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return redirect('conversation', username=username)

    return render(request, "messaging/conversation.html", {
        "messages": messages,
        "other_user": other_user
    })
