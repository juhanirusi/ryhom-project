from django.db import models


class ArticleQuerySet(models.QuerySet):
    def by_author(self, author):
        return self.filter(author=author)

    def published(self):
        return self.filter(status='Published')

    def by_category(self, category):
        return self.filter(categories=category)

    def by_tag(self, tag):
        return self.filter(tags=tag)

    def drafted(self):
        return self.filter(status='Saved For Later')

    def waiting_review(self):
        return self.filter(status='Wants To Publish')


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def by_author(self, author):
        return self.get_queryset().by_author(author)

    def published(self):
        return self.get_queryset().published()

    def by_category(self, category):
        return self.get_queryset().by_category(category)

    def by_tag(self, tag):
        return self.get_queryset().by_tag(tag)

    def drafted(self):
        return self.get_queryset().drafted()

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
