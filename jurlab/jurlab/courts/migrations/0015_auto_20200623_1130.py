# Generated by Django 3.0.7 on 2020-06-23 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courts', '0014_auto_20200623_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentscourts',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария'),
        ),
    ]
