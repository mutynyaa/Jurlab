# Generated by Django 2.2.11 on 2020-06-17 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0008_courtscomments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courtscomments',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='courts',
            name='comments',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courts.CourtsComments'),
        ),
    ]
