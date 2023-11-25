# Generated by Django 2.2.11 on 2020-07-03 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0024_auto_20200703_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courtdocuments',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='courtdocuments',
            name='object_id',
        ),
        migrations.AddField(
            model_name='courtdocuments',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='courts.Courts', verbose_name='Судебное дело'),
        ),
    ]