# Generated by Django 2.2.11 on 2020-07-07 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0004_delete_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supervisor',
            name='text',
        ),
        migrations.AddField(
            model_name='supervisor',
            name='court_author_vision',
            field=models.BooleanField(default=False),
        ),
    ]
