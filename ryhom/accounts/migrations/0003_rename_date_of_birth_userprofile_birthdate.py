# Generated by Django 4.0.5 on 2022-06-18 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_date_of_birth_alter_userprofile_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='date_of_birth',
            new_name='birthdate',
        ),
    ]
