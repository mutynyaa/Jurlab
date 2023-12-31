# Generated by Django 3.1 on 2020-11-05 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0095_auto_20201105_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='courts',
            name='state_duty_prognosis',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Сумма госпошлины (заявленная)'),
        ),
        migrations.AddField(
            model_name='courts',
            name='sum_amount_expertize_prognosis',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Сумма экспертизы (заявленная)'),
        ),
        migrations.AddField(
            model_name='historicalcourts',
            name='state_duty_prognosis',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Сумма госпошлины (заявленная)'),
        ),
        migrations.AddField(
            model_name='historicalcourts',
            name='sum_amount_expertize_prognosis',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Сумма экспертизы (заявленная)'),
        ),
    ]
