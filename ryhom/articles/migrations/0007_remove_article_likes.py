# Generated by Django 4.0.5 on 2022-07-04 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_alter_article_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='likes',
        ),
    ]
