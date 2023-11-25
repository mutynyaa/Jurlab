# Generated by Django 3.0.7 on 2020-07-11 09:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courts', '0029_courts_observer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courts',
            name='observer',
        ),
        migrations.AddField(
            model_name='courts',
            name='observer',
            field=models.ManyToManyField(blank=True, null=True, related_name='_courts_observer_+', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный'),
        ),
    ]
