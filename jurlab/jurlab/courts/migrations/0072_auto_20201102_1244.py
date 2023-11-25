# Generated by Django 3.1 on 2020-11-02 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0071_auto_20201102_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='courts',
            name='third_persons',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Третьи лица'),
        ),
        migrations.AddField(
            model_name='historicalcourts',
            name='third_persons',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Третьи лица'),
        ),
        migrations.AlterField(
            model_name='courts',
            name='defendant_peresentative',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Представитель ответчика'),
        ),
        migrations.AlterField(
            model_name='courts',
            name='plaintiff_peresentative',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Представитель Истца'),
        ),
        migrations.AlterField(
            model_name='historicalcourts',
            name='defendant_peresentative',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Представитель ответчика'),
        ),
        migrations.AlterField(
            model_name='historicalcourts',
            name='plaintiff_peresentative',
            field=models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='Представитель Истца'),
        ),
    ]
