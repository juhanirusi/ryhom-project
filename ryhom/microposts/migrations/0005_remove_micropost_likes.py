# Generated by Django 4.0.6 on 2022-07-12 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microposts', '0004_remove_micropost_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='micropost',
            name='likes',
        ),
    ]
