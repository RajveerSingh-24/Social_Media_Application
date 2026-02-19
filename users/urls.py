from django.urls import path
from . import views
from users.views import public_profile_view

urlpatterns = [
    path('signup/', views.register_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/', views.edit_profile_view, name='edit-profile'),
   path('u/<str:username>/', views.public_profile_view, name='public_profile'),

    # Follow / Unfollow
    path('follow/<int:user_id>/', views.follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow-user'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate-account'),
    path('resend-activation/', views.resend_activation, name='resend-activation'),
    path('enable-2fa/', views.enable_2fa, name='enable-2fa'),
    path('verify-2fa/', views.verify_2fa, name='verify-2fa'),
    path('2fa-login/', views.two_factor_login, name='2fa-login'),
    path('search/', views.user_search, name='user-search'),
    path('<str:username>/followers/', views.followers_list, name='followers-list'),
    path('<str:username>/following/', views.following_list, name='following-list'),


]

from django.contrib.auth import views as auth_views

urlpatterns += [

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
            email_template_name='emails/password_reset_email.txt',
            html_email_template_name='emails/password_reset_email.html',
            success_url='/accounts/password-reset/done/'
        ),
        name='password-reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password-reset-done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url='/accounts/password-reset/complete/'
        ),
        name='password-reset-confirm'
    ),

    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password-reset-complete'
    ),
]
