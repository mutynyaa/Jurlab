# Generated by Django 2.2.11 on 2020-07-03 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0022_auto_20200703_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courts',
            name='court_documents',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courts.CourtDocuments'),
        ),
    ]
