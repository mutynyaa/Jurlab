# Generated by Django 2.2.11 on 2020-07-29 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0007_auto_20200707_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='supervisor',
            name='ex_author_vision',
            field=models.BooleanField(default=False),
        ),
    ]