# Generated by Django 4.0.6 on 2022-07-11 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_alter_article_options_alter_articlecomment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255, unique=True),
        ),
    ]
