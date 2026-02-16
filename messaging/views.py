from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


@login_required
def inbox(request):
    conversations = request.user.conversations.all()

    return render(request, "messaging/inbox.html", {
        "conversations": conversations
    })


@login_required
def chat(request, username):
    other_user = get_object_or_404(User, username=username)

    # Find existing conversation between both users
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    # If conversation doesn't exist → create one
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    # Send message
    if request.method == "POST":
        content = request.POST.get("content")
        image = request.FILES.get("image")

        if content or image:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content,
                image=image
            )

            return redirect("chat", username=username)

    messages = conversation.messages.all().order_by("timestamp")

    return render(request, "messaging/chat.html", {
        "conversation": conversation,
        "messages": messages,
        "other_user": other_user
    })


