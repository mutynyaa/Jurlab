# Generated by Django 2.2.11 on 2020-06-29 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='department_date',
        ),
        migrations.RemoveField(
            model_name='position',
            name='position_date',
        ),
        migrations.AddField(
            model_name='profiles',
            name='position_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='position',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
    ]
