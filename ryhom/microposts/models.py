from django.conf import settings
from django.db import models
from django.urls import reverse

from ryhom.core.models import BaseAbstractModel, BaseCommentModel
from ryhom.core.utils import random_string_generator
from ryhom.tags.models import Tag

from .managers import MicropostCommentsManager, MicropostManager


class Micropost(BaseAbstractModel):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="micropost-images/")
    image_credit = models.CharField(blank=True, max_length=50)
    content = models.TextField(max_length=1700)
    tags = models.ManyToManyField(Tag, blank=True)
    published = models.BooleanField(default=False)
    slug = models.SlugField(default="", blank=True, null=False, unique=True)
    likers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="micropost_likes"
    )

    objects = models.Manager()
    microposts = MicropostManager()

    class Meta:
        db_table = "micropost"  # Good to define table name!
        verbose_name = "Micropost"
        verbose_name_plural = "Microposts"
        ordering = ["-created", "-modified"]

    def _create_slug(self):
        unique_slug = random_string_generator()
        while Micropost.objects.filter(slug=unique_slug).exists():
            unique_slug = random_string_generator()
            unique_slug = "{}".format(unique_slug)

        self.slug = unique_slug

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a URL slug for
        the article.
        """
        if self._state.adding is True:
            self._create_slug()
        super(Micropost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "microposts:micropost_detail", kwargs={"micropost_slug": self.slug}
        )

    def __str__(self):
        return self.title


class MicropostComment(BaseCommentModel):
    post = models.ForeignKey(Micropost, on_delete=models.CASCADE)
    likers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="micropost_comment_likes"
    )

    objects = models.Manager()
    micropost_comments = MicropostCommentsManager()

    class Meta:
        db_table = "micropost_comment"  # Good to define table name!
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created"]

    @property
    def child_comments(self):
        return MicropostComment.objects.filter(parent=self).all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return f"Comment by {self.author}"
