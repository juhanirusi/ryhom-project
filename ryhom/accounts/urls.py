from django.urls import path

from .views import ActivateAccountView, LoginView, RegisterView  # login_user

urlpatterns = [
    path('auth/create-account/', RegisterView.as_view(), name='create-account'),
    path('auth/activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),

    path('auth/login/', LoginView.as_view(), name='login'),
]
