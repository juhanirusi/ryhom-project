from django.db import models
from django.db.models import Q


class UserPostsManager(models.Manager):
    def published_articles(self, user):
        return self.get_queryset().filter(
            Q(status='Published') &
            Q(author=user)).order_by('-modified')

    def draft_articles(self, user):
        return self.get_queryset().filter(
            Q(status='Saved For Later') &
            Q(author=user)).order_by('-modified')

    def waiting_review_articles(self, user):
        return self.get_queryset().filter(
            Q(status='Wants To Publish') &
            Q(author=user)).order_by('-modified')
