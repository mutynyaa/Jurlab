# Generated by Django 3.1 on 2020-11-03 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0087_auto_20201103_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courts',
            name='type_proceedings_choises',
            field=models.IntegerField(choices=[(1, 'Гражданское судопроизводство'), (2, 'Уголовное судопроизводство'), (3, 'Административное судопроизводство')], default='Гражданское судопроизводство', verbose_name='Вид судопроизводства'),
        ),
        migrations.AlterField(
            model_name='historicalcourts',
            name='type_proceedings_choises',
            field=models.IntegerField(choices=[(1, 'Гражданское судопроизводство'), (2, 'Уголовное судопроизводство'), (3, 'Административное судопроизводство')], default='Гражданское судопроизводство', verbose_name='Вид судопроизводства'),
        ),
    ]
