# Generated by Django 3.1 on 2020-11-02 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0074_commentscourts_text_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentscourts',
            name='text_test',
        ),
    ]