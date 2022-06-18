from django.urls import path
from ryhom.layout import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
