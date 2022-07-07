from django.urls import path

from .views import AddArticleView, ArticleDetailView, UserPostsView

app_name = 'articles'

urlpatterns = [
    path('add-article', AddArticleView.as_view(), name='add_article'),
    path('my-posts', UserPostsView.as_view(), name='my_posts'),
    path('<slug:article_slug>', ArticleDetailView.as_view(), name='article_detail'),

    # path('post/<int:post_pk>/comment/<int:pk>/like', AddCommentLike.as_view(), name='comment-like'),
]
