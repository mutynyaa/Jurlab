# Generated by Django 3.1 on 2020-11-02 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0073_auto_20201102_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentscourts',
            name='text_test',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Текст комментария'),
        ),
    ]
