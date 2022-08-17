from django.db import models


class MicropostQuerySet(models.QuerySet):
    def by_author(self, author):
        return self.filter(author=author)

    def published(self):
        return self.filter(published=True)

    def by_tag(self, tag):
        return self.filter(tags=tag)


class MicropostManager(models.Manager):
    def get_queryset(self):
        return MicropostQuerySet(self.model, using=self._db)

    def by_author(self, author):
        return self.get_queryset().by_author(author)

    def published(self):
        return self.get_queryset().published()

# -------------------------------------------------------------------

class MicropostCommentsQuerySet(models.QuerySet):
    def user_comments(self, author):
        return self.filter(author=author)


class MicropostCommentsManager(models.Manager):
    def get_queryset(self):
        return MicropostCommentsQuerySet(self.model, using=self._db)

    def user_comments(self, author):
        return self.get_queryset().user_comments(author)
