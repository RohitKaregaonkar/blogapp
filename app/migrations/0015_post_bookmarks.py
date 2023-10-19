# Generated by Django 4.2.4 on 2023-10-19 05:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0014_websitemeta'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='bookmarks', to=settings.AUTH_USER_MODEL),
        ),
    ]
