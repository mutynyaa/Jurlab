# Generated by Django 2.2.11 on 2020-08-07 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0041_courts_arhive_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courts',
            name='arhive_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата перевода в архив'),
        ),
        migrations.AlterField(
            model_name='courts',
            name='created_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата создания'),
        ),
    ]