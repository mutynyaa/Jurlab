# Generated by Django 2.2.11 on 2020-07-10 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0015_profiles_is_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='only_their_courts',
            field=models.BooleanField(default=False),
        ),
    ]