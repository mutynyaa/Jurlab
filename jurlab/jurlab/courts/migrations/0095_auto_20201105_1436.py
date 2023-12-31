# Generated by Django 3.1 on 2020-11-05 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0094_auto_20201105_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='courts',
            name='total_sum_in_the_case',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Сумма экспертизы'),
        ),
        migrations.AddField(
            model_name='courts',
            name='total_sum_in_the_case_prognosis',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Сумма экспертизы'),
        ),
        migrations.AddField(
            model_name='historicalcourts',
            name='total_sum_in_the_case',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Сумма экспертизы'),
        ),
        migrations.AddField(
            model_name='historicalcourts',
            name='total_sum_in_the_case_prognosis',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Сумма экспертизы'),
        ),
    ]
