# Generated by Django 2.2.11 on 2020-07-03 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0019_courtsdocuments_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courtsdocuments',
            name='name',
            field=models.CharField(blank=True, default='nkdkd', max_length=200, null=True),
        ),
    ]
