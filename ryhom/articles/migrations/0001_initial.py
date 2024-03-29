# Generated by Django 4.0.6 on 2023-01-19 12:01

import ckeditor_uploader.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(5)])),
                ('summary', models.TextField(blank=True, max_length=255)),
                ('image', models.ImageField(blank=True, upload_to='article-thumbnails/')),
                ('image_credit', models.CharField(blank=True, max_length=50)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('type', models.CharField(choices=[('Article', 'Article'), ('Story', 'Story'), ('List', 'List'), ('Checklist', 'Checklist'), ('What if...', 'What If...'), ('Questions To Ask', 'Questions To Ask'), ('Myth-buster', 'Myth-buster'), ('Lesson-learned', 'Lesson-learned'), ('What People say', 'What People say')], default='Article', max_length=25)),
                ('featured', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('Saved For Later', 'Saved For Later'), ('Wants To Publish', 'Wants To Publish'), ('Published', 'Published')], default='Saved For Later', max_length=16)),
                ('slug', models.SlugField(blank=True, default='', max_length=255, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(blank=True, to='categories.category')),
                ('tags', models.ManyToManyField(blank=True, to='tags.tag')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ['-created', '-modified'],
                'unique_together': {('author', 'title')},
            },
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('comment', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('likers', models.ManyToManyField(blank=True, related_name='article_comments_likes', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='articles.articlecomment')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['-created'],
            },
        ),
    ]
