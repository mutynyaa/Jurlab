# Generated by Django 2.2.11 on 2020-07-07 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0005_auto_20200707_1544'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supervisor',
            old_name='court_author_vision',
            new_name='courtauthorvision',
        ),
    ]