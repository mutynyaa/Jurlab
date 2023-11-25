# Generated by Django 3.1 on 2020-11-02 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0068_auto_20201030_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='courts',
            name='sum_of_penalty',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма штрафа'),
        ),
        migrations.AddField(
            model_name='historicalcourts',
            name='sum_of_penalty',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма штрафа'),
        ),
        migrations.AlterField(
            model_name='courts',
            name='history_court_hearing',
            field=models.TextField(blank=True, default=None, max_length=2000, null=True, verbose_name='История судебных заседаний по делу'),
        ),
        migrations.AlterField(
            model_name='historicalcourts',
            name='history_court_hearing',
            field=models.TextField(blank=True, default=None, max_length=2000, null=True, verbose_name='История судебных заседаний по делу'),
        ),
    ]
