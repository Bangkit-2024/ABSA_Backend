# Generated by Django 5.0.5 on 2024-06-11 07:13

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=authentication.models.unique_filename),
        ),
    ]
