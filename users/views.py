from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import qrcode
from io import BytesIO

from .forms import LoginForm, RegisterForm, ProfileUpdateForm
from .models import Follow

User = get_user_model()


# ---------------- PUBLIC PROFILE ----------------

def public_profile_view(request, username):
    user_obj = get_object_or_404(
        User.objects.annotate(
            followers_count=Count('followers'),
            following_count=Count('following')
        ),
        username__iexact=username
    )

    is_self = request.user == user_obj if request.user.is_authenticated else False

    is_following = False
    if request.user.is_authenticated and not is_self:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user_obj
        ).exists()

    context = {
        'user_obj': user_obj,
        'is_self': is_self,
        'is_following': is_following,
    }

    return render(request, 'users/public_profile.html', context)


# ---------------- LOGIN ----------------

def login_view(request):
    if request.user.is_authenticated:
        return redirect('user-profile', username=request.user.username)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:

                # If 2FA enabled → go to OTP step
                if user.is_2fa_enabled:
                    request.session['pre_2fa_user_id'] = user.id
                    return redirect('2fa-login')

                # Normal login
                login(request, user)
                return redirect('user-profile', username=user.username)

            # Authentication failed
            messages.error(request, "Invalid credentials")

    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


# ---------------- REGISTER ----------------

def register_view(request):
    if request.user.is_authenticated:
        return redirect('user-profile', username=request.user.username)

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            activation_link = request.build_absolute_uri(
                reverse('activate-account', kwargs={
                    'uidb64': uid,
                    'token': token
                })
            )

            context = {
                'user': user,
                'activation_link': activation_link,
            }

            text_content = render_to_string(
                'emails/activation_email.txt', context
            )
            html_content = render_to_string(
                'emails/activation_email.html', context
            )

            email = EmailMultiAlternatives(
                "Activate Your Account",
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(
                request,
                "Check your email to activate your account."
            )
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


# ---------------- ACTIVATE ACCOUNT ----------------

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated successfully.")
        return redirect('login')

    messages.error(request, "Activation link is invalid or expired.")
    return redirect('signup')


# ---------------- 2FA ----------------

@login_required
def enable_2fa(request):
    user = request.user

    if not user.otp_secret:
        user.generate_otp_secret()

    totp_uri = user.get_totp_uri()

    qr = qrcode.make(totp_uri)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    return HttpResponse(buffer.getvalue(), content_type="image/png")


@login_required
def verify_2fa(request):
    if request.method == "POST":
        otp = request.POST.get("otp")

        if request.user.verify_otp(otp):
            request.user.is_2fa_enabled = True
            request.user.save()
            messages.success(request, "2FA enabled successfully.")
            return redirect('user-profile', username=request.user.username)

        messages.error(request, "Invalid OTP.")

    return render(request, "users/verify_2fa.html")


def two_factor_login(request):
    user_id = request.session.get('pre_2fa_user_id')

    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        otp = request.POST.get("otp")

        if user.verify_otp(otp):
            login(request, user, backend='users.backends.EmailOrUsernameBackend')
            del request.session['pre_2fa_user_id']
            return redirect('user-profile', username=user.username)

        messages.error(request, "Invalid OTP.")

    return render(request, "users/2fa_login.html")


# ---------------- LOGOUT ----------------

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


# ---------------- EDIT PROFILE ----------------

@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user-profile', username=request.user.username)

    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})


# ---------------- FOLLOW SYSTEM ----------------

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)

    if user_to_follow != request.user:
        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

    return redirect('user-profile', username=user_to_follow.username)


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)

    Follow.objects.filter(
        follower=request.user,
        following=user_to_unfollow
    ).delete()

    return redirect('user-profile', username=user_to_unfollow.username)

def resend_activation(request):
    if request.user.is_authenticated:
        messages.info(request, "Your account is already active.")
        return redirect('user-profile', username=request.user.username)

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email__iexact=email)

            if user.is_active:
                messages.info(request, "Account already activated.")
                return redirect('login')

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            activation_link = request.build_absolute_uri(
                reverse('activate-account', kwargs={
                    'uidb64': uid,
                    'token': token
                })
            )

            context = {
                'user': user,
                'activation_link': activation_link,
            }

            text_content = render_to_string(
                'emails/activation_email.txt', context
            )
            html_content = render_to_string(
                'emails/activation_email.html', context
            )

            email_message = EmailMultiAlternatives(
                "Activate Your Account",
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )

            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            messages.success(request, "Activation email resent.")

        except User.DoesNotExist:
            messages.success(request, "If the email exists, activation email has been sent.")

        return redirect('login')

    return render(request, "users/resend_activation.html")
