# Generated by Django 2.2.11 on 2020-08-03 05:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0037_delete_courtscomments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courts',
            name='observer',
            field=models.ManyToManyField(blank=True, related_name='obs', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный'),
        ),
        migrations.CreateModel(
            name='CourtJudgment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('court_judjment', models.FileField(upload_to='Courtjudgment/')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='judgment', to='courts.Courts', verbose_name='Судебное дело')),
            ],
        ),
    ]
