from django.db import models


class ArticleQuerySet(models.QuerySet):
    def by_author(self, author):
        return self.filter(author=author)

    def published_articles(self):
        return self.filter(status='Published').order_by('-modified')

    def draft_articles(self):
        return self.filter(status='Saved For Later').order_by('-modified')

    def waiting_review(self):
        return self.filter(status='Wants To Publish').order_by('-modified')


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def by_author(self, author):
        return self.get_queryset().by_author(author)

    def published_articles(self):
        return self.get_queryset().published_articles()

    def draft_articles(self):
        return self.get_queryset().draft_articles()

    def waiting_review(self):
        return self.get_queryset().waiting_review()

# -------------------------------------------------------------------

class ArticleCommentsQuerySet(models.QuerySet):
    def user_comments(self, author):
        return self.filter(author=author)


class ArticleCommentsManager(models.Manager):
    def get_queryset(self):
        return ArticleCommentsQuerySet(self.model, using=self._db)

    def user_comments(self, author):
        return self.get_queryset().user_comments(author)
