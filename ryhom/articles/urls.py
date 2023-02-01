from django.urls import path

from .views import (AddArticleView, AddRemoveArticleCommentLike,
                    ArticleDetailView, DeleteArticleView, EditArticleView)

app_name = 'articles'

urlpatterns = [
    path(
        'add-article',
        AddArticleView.as_view(),
        name='add_article'
    ),
    path(
        'edit-article/<uuid:article_uuid>',
        EditArticleView.as_view(),
        name='edit_article'
    ),
    path(
        'delete-article/<uuid:article_uuid>',
        DeleteArticleView.as_view(),
        name='delete_article'
    ),

    path(
        '<slug:article_slug>',
        ArticleDetailView.as_view(),
        name='article_detail'
    ),
    path(
        '<int:article_pk>/comment/<int:pk>/like',
        AddRemoveArticleCommentLike.as_view(),
        name='article_comment_like_unlike'
    ),
]
