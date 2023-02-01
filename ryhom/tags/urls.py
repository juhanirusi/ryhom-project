from django.urls import path

from .views import ArticlesByTagListView, MicropostsByTagListView

app_name = 'tags'

urlpatterns = [
    path(
        'articles/<slug:tag_slug>',
        ArticlesByTagListView.as_view(),
        name='articles_by_tag'
    ),
    path(
        'microposts/<slug:tag_slug>',
        MicropostsByTagListView.as_view(),
        name='microposts_by_tag'
    ),
]
