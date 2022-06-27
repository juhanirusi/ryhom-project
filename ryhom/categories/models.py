import itertools

from django.db import models
from django.utils.text import slugify

#from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, default='', blank=True)
    slug = models.SlugField(unique=True, null=False, default='', blank=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='sub_categories'
    )

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def _generate_slug(self):
        value = self.name
        slug_candidate = slug_original = slugify(value)
        for i in itertools.count(1):
            if not Category.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        parent = self.parent
        while parent is not None:
            if parent == self:
                raise RuntimeError("Circular references not allowed")
            parent = parent.parent

        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("categories:category", kwargs={'slug': self.slug})

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])
