from django.urls import path

from .views import (AccountSettingsView, ActivateAccountView, ChangeEmailView,
                    ChangePasswordView, LoginUserView, LogoutUserView,
                    RegisterView, ResendActivationEmailView,
                    ResetPasswordConfirmationView, ResetPasswordDoneView,
                    ResetPasswordMessageView, ResetPasswordView, UserPostsView,
                    UserProfileView)

app_name = 'accounts'

urlpatterns = [
    path(
        'auth/create-account',
        RegisterView.as_view(),
        name='create_account'
    ),
    path(
        'auth/activate/<uidb64>/<token>',
        ActivateAccountView.as_view(),
        name='activate'
    ),
    path(
        'auth/resend-activitation-email',
        ResendActivationEmailView.as_view(),
        name='resend_activation_email'
    ),
    path(
        'auth/login',
        LoginUserView.as_view(),
        name='login'
    ),
    path(
        'auth/logout',
        LogoutUserView.as_view(),
        name='logout'
    ),
    path(
        'auth/password-reset',
        ResetPasswordView.as_view(),
        name='password_reset'
    ),
    path(
        'auth/password-reset/message',
        ResetPasswordMessageView.as_view(),
        name='password_reset_message',
    ),
    path(
        'auth/password-reset-confirm/<uidb64>/<token>',
        ResetPasswordConfirmationView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'auth/password-reset/done',
        ResetPasswordDoneView.as_view(),
        name='password_reset_done',
    ),

    path(
        'account/settings',
        AccountSettingsView.as_view(),
        name='account_settings'
    ),
    path(
        'account/my-posts',
        UserPostsView.as_view(),
        name='my_posts'
    ),
    path(
        '<slug:user_profile_slug>',
        UserProfileView.as_view(),
        name='user_profile'
    ),

    path(
        'account/settings/password/change',
        ChangePasswordView.as_view(),
        name='change_password'
    ),
    path(
        'account/settings/email/change',
        ChangeEmailView.as_view(),
        name='change_email'
    ),
]
