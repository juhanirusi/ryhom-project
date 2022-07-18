import itertools

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ryhom.categories.models import Category
from ryhom.core.models import BaseAbstractModel, BaseCommentModel
from ryhom.tags.models import Tag

from .managers import ArticleCommentsManager, ArticleManager


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

    class Status(models.TextChoices):
        WRITER_SAVED_FOR_LATER = 'Saved For Later', 'Saved For Later'
        WRITER_WANTS_TO_PUBLISH = 'Wants To Publish', 'Wants To Publish'
        PUBLISHED = 'Published', 'Published'

    title = models.CharField(max_length=150,
        validators=[MinLengthValidator(5)]
    )
    summary = models.TextField(max_length=255, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField(blank=True, upload_to='article-thumbnails/')
    image_credit = models.CharField(blank=True, max_length=50)
    content = RichTextUploadingField(config_name='custom_editor', blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    type = models.CharField(max_length=25, choices=Type.choices,
        default=Type.ARTICLE
    )
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices=Status.choices,
        default=Status.WRITER_SAVED_FOR_LATER
    )
    slug = models.SlugField(
        default='', max_length=255, blank=True, null=False, unique=True)

    objects = models.Manager()
    articles = ArticleManager()

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-created', '-modified']
        # 1 author can't have multiple articles with same title
        unique_together = ('author', 'title')


    def _create_slug(self):
        """
        To generate a unique URL slug we slugify the title of the article,
        then check if the slug already exists in the database, if it does
        we'll add a number (article-slug = article-slug-1) after the
        slug to generate a unique slug, then check again if the slug
        exists and continue this until a unique slug is generated.
        """
        slug = unique_slug = slugify(self.title) # Same value to 2 variables

        for num in itertools.count(1):
            if not Article.objects.filter(slug=unique_slug).exists():
                break
            unique_slug = '{}-{}'.format(slug, num)

        self.slug = unique_slug


    def save(self, *args, **kwargs):
        """
        Override the save method to generate a URL slug for
        the article.
        """
        if self._state.adding is True:
            self._create_slug()
        super(Article, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse(
            'articles:article_detail', kwargs={'article_slug': self.slug}
        )


    def __str__(self):
        return self.title


class ArticleComment(BaseCommentModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    likers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='article_comments'
    )

    objects = models.Manager()
    article_comments = ArticleCommentsManager()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering=['-created']


    @property
    def child_comments(self):
        return ArticleComment.objects.filter(parent=self).all()


    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


    def __str__(self):
        return f'Comment by {self.author}'
