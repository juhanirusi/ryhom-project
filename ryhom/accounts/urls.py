from django.urls import path

from .views import (AccountSettingsView, ActivateAccountView, ChangeEmailView,
                    ChangePasswordView, LoginUserView, LogoutUserView,
                    RegisterView, ResetPasswordConfirmation, ResetPasswordView,
                    UserProfileView, user_profile_redirect)

app_name = 'accounts'

urlpatterns = [
    path(
        'auth/create-account/',
        RegisterView.as_view(),
        name='create_account'
    ),
    path(
        'auth/activate/<uidb64>/<token>/',
        ActivateAccountView.as_view(),
        name='activate'
    ),
    path(
        'auth/login/',
        LoginUserView.as_view(),
        name='login'
    ),
    path(
        'auth/logout/',
        LogoutUserView.as_view(),
        name='logout'
    ),
    path(
        'auth/password-reset/',
        ResetPasswordView.as_view(),
        name='password_reset'
    ),
    path(
        'auth/password-reset-confirm/<uidb64>/<token>/',
        ResetPasswordConfirmation.as_view(),
        name='password_reset_confirm'
    ),

    path(
        'account/settings/',
        AccountSettingsView.as_view(),
        name='account_settings'
    ),
    path(
        '<slug:slug>',
        UserProfileView.as_view(),
        name='user_profile'
    ),
    path('profile-redirect/', user_profile_redirect),

    path(
        'account/settings/password/change/',
        ChangePasswordView.as_view(),
        name='change_password'
    ),
    path(
        'account/settings/email/change/',
        ChangeEmailView.as_view(),
        name='change_email'
    ),
]
