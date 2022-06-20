from django.urls import path

from .views import ActivateAccountView, RegisterView, login_user

urlpatterns = [
    path('auth/create-account/', RegisterView.as_view(), name='create-account'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),

    path('auth/login/', login_user, name='login'),
]
