# Generated by Django 3.0.7 on 2020-07-11 10:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courts', '0030_auto_20200711_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourtsObservers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observers', models.ManyToManyField(blank=True, null=True, related_name='_courtsobservers_observers_+', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный')),
            ],
        ),
        migrations.AlterField(
            model_name='courts',
            name='observer',
            field=models.ManyToManyField(blank=True, null=True, related_name='_courts_observer_+', to='courts.CourtsObservers', verbose_name='Ответственный'),
        ),
    ]
