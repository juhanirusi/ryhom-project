# Generated by Django 4.0.6 on 2022-07-18 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microposts', '0002_micropostcomment_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='micropostcomment',
            old_name='likes',
            new_name='likers',
        ),
    ]