# Generated by Django 2.2.11 on 2020-06-25 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0016_auto_20200623_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courts',
            name='result_of_win',
            field=models.BooleanField(null=True, verbose_name='Победа/Поражение'),
        ),
    ]
