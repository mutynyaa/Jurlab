# Generated by Django 3.1 on 2020-11-03 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0082_auto_20201103_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='courts',
            name='date_create_object_model',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalcourts',
            name='date_create_object_model',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
