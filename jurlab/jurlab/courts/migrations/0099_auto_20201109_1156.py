# Generated by Django 3.1 on 2020-11-09 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0098_auto_20201109_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courts',
            name='court_result',
            field=models.BooleanField(choices=[(1, 'Решение суда отсутствует'), (2, 'Решение суда вынесено в нашу пользу'), (3, 'Решение суда вынесено не в нашу пользу')], default=1, verbose_name='Победа/Поражение'),
        ),
        migrations.AlterField(
            model_name='courts',
            name='type_of_decision_civil',
            field=models.IntegerField(blank=True, choices=[(0, 'Решение судом не принято'), (1, 'Удовлетворение требований Истца в полном объеме'), (2, 'Частичное удовлетворение требований Истца'), (3, 'Отказ в удовлетворении требований'), (4, 'Отказ в принятии искового заявления'), (5, 'Оставление искового заявления без движения'), (6, 'Возвращение искового заявления')], default=0, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='courts',
            name='type_of_decision_criminal',
            field=models.IntegerField(blank=True, choices=[(0, 'Приговор не вынесен'), (1, 'Обвинительный приговор'), (2, 'Оправдательный приговор')], default=0, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='historicalcourts',
            name='court_result',
            field=models.BooleanField(choices=[(1, 'Решение суда отсутствует'), (2, 'Решение суда вынесено в нашу пользу'), (3, 'Решение суда вынесено не в нашу пользу')], default=1, verbose_name='Победа/Поражение'),
        ),
        migrations.AlterField(
            model_name='historicalcourts',
            name='type_of_decision_civil',
            field=models.IntegerField(blank=True, choices=[(0, 'Решение судом не принято'), (1, 'Удовлетворение требований Истца в полном объеме'), (2, 'Частичное удовлетворение требований Истца'), (3, 'Отказ в удовлетворении требований'), (4, 'Отказ в принятии искового заявления'), (5, 'Оставление искового заявления без движения'), (6, 'Возвращение искового заявления')], default=0, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='historicalcourts',
            name='type_of_decision_criminal',
            field=models.IntegerField(blank=True, choices=[(0, 'Приговор не вынесен'), (1, 'Обвинительный приговор'), (2, 'Оправдательный приговор')], default=0, verbose_name=''),
        ),
    ]
