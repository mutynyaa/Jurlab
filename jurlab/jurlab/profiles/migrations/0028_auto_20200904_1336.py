# Generated by Django 3.1 on 2020-09-04 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0027_auto_20200904_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mysession',
            name='session_key',
            field=models.CharField(max_length=100),
        ),
    ]
