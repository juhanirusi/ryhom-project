# Generated by Django 4.0.5 on 2022-07-07 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microposts', '0002_alter_micropost_content_alter_micropost_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='micropost',
            options={'ordering': ['-created', '-modified'], 'verbose_name': 'Micropost', 'verbose_name_plural': 'Microposts'},
        ),
        migrations.AlterModelOptions(
            name='micropostcomment',
            options={'ordering': ['-created'], 'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
    ]
