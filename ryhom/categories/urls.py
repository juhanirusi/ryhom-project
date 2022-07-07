from django.urls import path

from .views import CategoryDetailView

app_name = 'categories'

urlpatterns = [
    path('<slug:category_slug>', CategoryDetailView.as_view(), name='category_detail'),
]
