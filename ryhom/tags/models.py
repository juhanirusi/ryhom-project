import itertools

from django.db import models
from django.utils.text import slugify
from ryhom.categories.models import Category


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, default='', blank=True)
    slug = models.SlugField(unique=True, null=False, default='', blank=True)
    categories = models.ManyToManyField(Category)


    def _generate_slug(self):
        name = self.name
        unique_slug = slug = slugify(name) # Same value to 2 variables

        for num in itertools.count(1):
            if not Category.objects.filter(slug=unique_slug).exists():
                break
            unique_slug = '{}{}'.format(slug, num)

        self.slug = unique_slug


    def save(self, *args, **kwargs):

        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
