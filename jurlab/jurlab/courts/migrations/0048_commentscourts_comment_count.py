# Generated by Django 3.1 on 2020-09-24 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0047_auto_20200820_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentscourts',
            name='comment_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]