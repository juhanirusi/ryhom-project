from django.urls import path

from .views import (AccountSettingsView, ActivateAccountView,
                    ChangePasswordView, LoginUserView, LogoutUserView,
                    RegisterView, UserProfileView, user_profile_redirect)

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
]
