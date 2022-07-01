from django.conf import settings
from django.db import models
from ryhom.categories.models import Category
from ryhom.core.models import BaseAbstractModel
from ryhom.tags.models import Tag


class Micropost(BaseAbstractModel):

    class Type(models.TextChoices):
        TEXT = 'Text', 'Text'
        IMAGE = 'Image', 'Image'

    title = models.CharField(max_length=255, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='micropost-images/')
    image_credit = models.CharField(blank=True, max_length=50)
    content = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    type = models.CharField(max_length=25, choices=Type.choices, default=Type.TEXT)
    likes = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)
    slug = models.SlugField(default='', blank=True, null=False, unique=True)

    def __str__(self):
        return self.title
