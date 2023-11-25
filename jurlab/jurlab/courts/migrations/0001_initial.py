# Generated by Django 2.2.11 on 2020-06-10 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourtsInstanse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('court_instanse_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CourtsJudgment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('court_judgment', models.CharField(max_length=200, verbose_name='Решение суда')),
            ],
        ),
        migrations.CreateModel(
            name='CourtsStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('court_status_name', models.CharField(max_length=200, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='Courts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('court_name', models.CharField(max_length=200, verbose_name='Наименование суда')),
                ('plaintiff', models.CharField(max_length=200, verbose_name='Истец')),
                ('defendant', models.CharField(max_length=200, verbose_name='Ответчик')),
                ('lawsuit_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма иска')),
                ('result_of_win', models.BooleanField(verbose_name='Победа/Поражение')),
                ('win_amount_main', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма выигрыша по основному требованию')),
                ('defeat_amount_main', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма проигрыша по основному требованию')),
                ('win_amount_expected_additional', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма заявленная за юридические услуги')),
                ('win_amount_additional', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма выигрыша по юр. услугам')),
                ('defeat_amount_additional', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма проигрыша по юр. услугам')),
                ('text', models.TextField()),
                ('instanse', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courts.CourtsInstanse')),
                ('jungment', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courts.CourtsJudgment')),
                ('status', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courts.CourtsStatus')),
            ],
        ),
    ]