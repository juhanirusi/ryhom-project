from django.urls import path

from .views import IndexView, user_profile_redirect

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('profile-redirect/', user_profile_redirect),
]
