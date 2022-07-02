# Generated by Django 4.0.5 on 2022-07-01 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0002_category_icon'),
        ('tags', '0002_tag_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Micropost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('image', models.ImageField(blank=True, upload_to='micropost-images/')),
                ('image_credit', models.CharField(blank=True, max_length=50)),
                ('content', models.TextField(blank=True)),
                ('type', models.CharField(choices=[('Text', 'Text'), ('Image', 'Image')], default='Text', max_length=25)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('published', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, default='', unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(blank=True, to='categories.category')),
                ('tags', models.ManyToManyField(blank=True, to='tags.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]