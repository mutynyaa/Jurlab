# Generated by Django 3.1 on 2020-09-28 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0055_courts_read_court_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='courts',
            name='comment_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
