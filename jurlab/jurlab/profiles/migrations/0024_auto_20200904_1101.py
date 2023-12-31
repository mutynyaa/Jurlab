# Generated by Django 3.1 on 2020-09-04 04:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0023_connectionhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='MySession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_board', models.CharField(max_length=1024)),
                ('expire_date', models.DateTimeField()),
                ('active', models.CharField(blank=True, max_length=1024)),
                ('thread', models.TextField(blank=True)),
                ('session_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions.session')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='ConnectionHistory',
        ),
    ]
