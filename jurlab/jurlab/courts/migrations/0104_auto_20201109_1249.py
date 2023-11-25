# Generated by Django 3.1 on 2020-11-09 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0103_auto_20201109_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courts',
            name='court_result',
            field=models.IntegerField(blank=True, choices=[(None, 'Решение суда отсутствует'), (1, 'Решение суда вынесено в нашу пользу'), (2, 'Решение суда вынесено не в нашу пользу')], default=None, null=True, verbose_name='Победа/Поражение'),
        ),
        migrations.AlterField(
            model_name='historicalcourts',
            name='court_result',
            field=models.IntegerField(blank=True, choices=[(None, 'Решение суда отсутствует'), (1, 'Решение суда вынесено в нашу пользу'), (2, 'Решение суда вынесено не в нашу пользу')], default=None, null=True, verbose_name='Победа/Поражение'),
        ),
    ]
