from django.urls import path

from .views import AddArticleView

app_name = 'articles'

urlpatterns = [
    path('add-article/', AddArticleView.as_view(), name='add_article'),
]
