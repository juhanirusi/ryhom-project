from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify
from ryhom.categories.models import Category
from ryhom.core.models import BaseAbstractModel
from ryhom.core.utils import random_string_generator
from ryhom.tags.models import Tag


class Article(BaseAbstractModel):
    """
    Model for articles.
    """

    class Type(models.TextChoices):
        ARTICLE = 'Article', 'Article'
        STORY = 'Story', 'Story'
        LISTICLE = 'List', 'List'
        CHECKLIST = 'Checklist', 'Checklist'
        WHAT_IF = 'What if...', 'What If...'
        QUESTIONS_TO_ASK = 'Questions To Ask', 'Questions To Ask'
        MYTH_BUSTER = 'Myth-buster', 'Myth-buster'
        LESSON_LEARNED = 'Lesson-learned', 'Lesson-learned'
        PEOPLE_SAYING = 'What People say', 'What People say'

    title = models.CharField(max_length=150, validators=[MinLengthValidator(5)])
    summary = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='article-images/')
    image_credit = models.CharField(blank=True, max_length=50)
    content = RichTextUploadingField(config_name='custom_editor')
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    type = models.CharField(max_length=25, choices=Type.choices, default=Type.ARTICLE)
    featured = models.BooleanField(default=False)
    likes = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)
    slug = models.SlugField(default='', blank=True, null=False, unique=True)

    class Meta:
        ordering = ['-created', '-modified']
        unique_together = ('author', 'title') # 1 author can't have multiple articles with same title

        # ASSIGN THE DEFAULT MODEL MANAGER BEFORE OUR CUSTOM ONES!
        #objects = models.Manager()


    # def total_likes(self):
    #     return self.likes.count()


    def _create_slug(self):
        """
        Remove all whitespace from the name. Then check if slug
        already exists in the database. If it does exists, add
        a number after the slug until the database doesn't
        contain any other matching slug.
        """
        slug = unique_slug = slugify(self.title)
        random_string = random_string_generator()
        unique_slug = '{}-{}'.format(slug, random_string)

        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, random_string_generator())

        self.slug = unique_slug


    def save(self, *args, **kwargs):
        """Override the save method to generate a URL slug, or check if a duplicate slug exists and generate a new one for the article"""
        if self._state.adding is True:
            self._create_slug()
        super(Article, self).save(*args, **kwargs)


    def __str__(self):
        return self.title


class Comment(BaseAbstractModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    comment = models.TextField() # <-- ADD A VALIDATOR TO FORM (50 to 6,000 CHARACTERS!)
    likes = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", null=True, blank=True)

    class Meta:
        ordering=["-created"]

    # @property
    # def child_comments(self):
    #     return Comment.objects.filter(parent=self).reverse()

    # @property
    # def is_parent(self):
    #     if self.parent is None:
    #         return True
    #     return False

    def __str__(self):
        return f'Comment by {self.author}'
