# Generated by Django 4.0.6 on 2022-07-11 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_article_likes_articlecomment_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='articlecomment',
            name='likes',
        ),
    ]
