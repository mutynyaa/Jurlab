# Generated by Django 2.2.11 on 2020-06-29 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20200629_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='work_is_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]