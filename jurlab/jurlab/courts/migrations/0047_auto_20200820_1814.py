# Generated by Django 3.1 on 2020-08-20 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0046_auto_20200820_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courts',
            name='date_getting_lawsuit',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Дата получения/подачи искового заявления'),
        ),
    ]
