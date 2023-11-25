# Generated by Django 2.2.11 on 2020-07-16 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('execution', '0002_auto_20200716_1230'),
    ]

    operations = [
        migrations.RenameField(
            model_name='executions',
            old_name='court_phone',
            new_name='agency_phone',
        ),
        migrations.AlterField(
            model_name='executions',
            name='exact',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Взыскано'),
        ),
    ]