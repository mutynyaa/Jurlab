# Generated by Django 2.2.11 on 2020-08-07 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0039_auto_20200807_1441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courts',
            name='arhive_date',
        ),
    ]
