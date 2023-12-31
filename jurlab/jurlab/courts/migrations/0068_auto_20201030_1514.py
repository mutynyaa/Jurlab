# Generated by Django 3.1 on 2020-10-30 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0067_auto_20201030_1444'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courts',
            old_name='win_amount_additional',
            new_name='sum_amount_additional',
        ),
        migrations.RenameField(
            model_name='courts',
            old_name='win_amount_expected_additional',
            new_name='sum_amount_expected_additional',
        ),
        migrations.RenameField(
            model_name='courts',
            old_name='win_amount_expertize',
            new_name='sum_amount_expertize',
        ),
        migrations.RenameField(
            model_name='courts',
            old_name='win_amount_penalty_agent',
            new_name='sum_amount_penalty_agent',
        ),
        migrations.RenameField(
            model_name='historicalcourts',
            old_name='win_amount_additional',
            new_name='sum_amount_additional',
        ),
        migrations.RenameField(
            model_name='historicalcourts',
            old_name='win_amount_expected_additional',
            new_name='sum_amount_expected_additional',
        ),
        migrations.RenameField(
            model_name='historicalcourts',
            old_name='win_amount_expertize',
            new_name='sum_amount_expertize',
        ),
        migrations.RenameField(
            model_name='historicalcourts',
            old_name='win_amount_penalty_agent',
            new_name='sum_amount_penalty_agent',
        ),
    ]
