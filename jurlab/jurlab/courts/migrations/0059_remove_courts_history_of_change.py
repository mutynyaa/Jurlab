# Generated by Django 3.1 on 2020-09-30 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0058_courts_history_of_change'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courts',
            name='history_of_change',
        ),
    ]
