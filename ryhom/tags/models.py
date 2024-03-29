import itertools

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from ryhom.categories.models import Category


class Tag(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(blank=True, upload_to="tag-icons/")
    description = models.TextField(max_length=300, default="", blank=True)
    slug = models.SlugField(unique=True, null=False, default="", blank=True)

    class Meta:
        db_table = "tag"  # Good to define table name!
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def _generate_slug(self):
        name = self.name
        unique_slug = slug = slugify(name)  # Same value to 2 variables

        for num in itertools.count(1):
            if not Category.objects.filter(slug=unique_slug).exists():
                break
            unique_slug = "{}{}".format(slug, num)

        self.slug = unique_slug

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tags:microposts_by_tag", kwargs={"tag_slug": self.slug})
        # If statement with...
        # return reverse('tags:articles_by_tag', kwargs={'tag_slug': self.slug})
        # when clicking tag in article detail page.

    def __str__(self):
        return self.name
