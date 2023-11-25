from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
import os
from simple_history.models import HistoricalRecords
from django.utils import timezone

# Константы аргумента choices модели courts

CHOICE_COURT_RESULT_CIVIL_AND_ADMINISTRICAL_PROCEEDINGS_AND_ADMINISTRICAL_OFFENCE = (
    (1, "Удовлетворение требований Истца в полном объеме"),
    (2, "Частичное удовлетворение требований Истца"),
    (3, "Отказ в удовлетворении требований"),
    (4, "Отказ в принятии искового заявления"),
    (5, "Оставление искового заявления без движения"),
    (6, "Возвращение искового заявления"),
)

CHOICE_COURT_RESULT_CRIMINAL = (
    (None, "Приговор не вынесен"),
    (1, "Обвинительный приговор"),
    (2, "Оправдательный приговор"),
)

CHOICE_COURT_RESULT = (
    (None, "Решение суда отсутствует"),
    (1, "Решение суда вынесено в нашу пользу"),
    (2, "Решение суда вынесено не в нашу пользу")
)

CHOICES_TYPE_PROCEEDINGS = (
    (1, "Гражданское судопроизводство"),
    (2, "Уголовное судопроизводство"),
    (3, "Административное судопроизводство"),
    (4, "Производство по делам об адмп. правонарушении"),
)

CHOICES_COURT_INSTANSE = (
    (1, "Первая инстанция"),
    (2, "Апелляционная инстанция"),
    (3, "Кассационная инстанция"),
    (4, "Надзорная инстанция"),
)

CHOICES_COURT_JURISDICTION = (
    (1, "Суды общей юрисдикции"),
    (2, "Арбитражные суды"),
    (3, "Третейские суды"),

)

class CourtsCategory(models.Model):
    court_instanse_name = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.court_instanse_name

        
class CourtsStatus(models.Model):
    court_status_name = models.CharField('Статус', max_length = 200)
    
    def __str__(self):
        return self.court_status_name
        
class CourtsJudgment(models.Model):
    court_judgment = models.CharField('Решение суда', max_length = 200)
    
    def __str__(self):
        return self.court_judgment




class Courts(models.Model):
    # Информация о суде
    court_name = models.CharField('Наименование суда', max_length=200, blank=True, null=True, default=None)
    case_number = models.CharField('№ дела', max_length=200, blank=True, null=True, default=None)
    court_address = models.CharField('Адрес (местонахождение) суда', max_length=200, blank=True, null=True,default=None)
    court_phone = models.CharField('№ телефона суда', max_length=200, blank=True, null=True, default=None)

    # Информация о судебном деле
        # Общая
    instance = models.IntegerField('Судебная инстанция', blank=True, null=True, default=None,choices=CHOICES_COURT_INSTANSE)
    status = models.ForeignKey(CourtsStatus, blank=True, null=True, default=None, on_delete=models.CASCADE)
    jurisdiction = models.IntegerField('Подведомственность (Юрисдикция)', blank=True, null=True, default=None,choices=CHOICES_COURT_JURISDICTION)
    category = models.ForeignKey(CourtsCategory, blank=True, null=True, default=None, on_delete=models.CASCADE)
    type_proceedings_choises = models.IntegerField('Вид судопроизводства', choices=CHOICES_TYPE_PROCEEDINGS, null=False)
    date_getting_lawsuit = models.DateField('Дата получения/подачи искового заявления (возбуждения уголовного дела)', blank=True, null=True,default=None)
    plaintiff = models.CharField('Истец / Потерпевший', max_length=200, null=False)
    plaintiff_representative = models.CharField('Представитель Истца / Потерпевшего', max_length=200, blank=True, null=True,default=None)
    defendant = models.CharField('Ответчик / Подсудимый', max_length=200, null=False)
    defendant_representative = models.CharField('Представитель ответчика / Подсудимого', max_length=200, blank=True, null=True,default=None)
    third_persons = models.CharField('Третьи лица', max_length=200, blank=True, null=True, default=None)
    text = models.TextField('Комментарий', blank=True, null=True)
    court_result = models.IntegerField('Победа/Поражение', default=None, blank=True, null=True,choices=CHOICE_COURT_RESULT)
    actual_court_hearing = models.DateTimeField('Ближайшее судебное заседание', max_length=200, blank=True, null=True,default=None)
    history_court_hearing = models.TextField('История судебных заседаний по делу', max_length=2000, blank=True,null=True, default=None)
        # Гражданские дела / административное судопроизводство
    type_of_decision_civil = models.IntegerField('', blank=True, null=True, default=None,choices=CHOICE_COURT_RESULT_CIVIL_AND_ADMINISTRICAL_PROCEEDINGS_AND_ADMINISTRICAL_OFFENCE)
        # Уголовные дела
    type_of_decision_criminal = models.IntegerField('', blank=True, null=True, default=None,choices=CHOICE_COURT_RESULT_CRIMINAL)

    # Суммы в судебном деле
    lawsuit_amount = models.DecimalField('Сумма иска', max_digits=10, decimal_places=2, default=0)
    state_duty = models.DecimalField('Сумма госпошлины', max_digits=10, decimal_places=2, default=0, blank=True,null=True)
    state_duty_prognosis = models.DecimalField('Сумма госпошлины (заявленная)', max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    sum_amount_main_prognosis = models.DecimalField('Сумма по основному требованию (заявленная)', max_digits=10,decimal_places=2, default=0, blank=True, null=True)
    sum_amount_main = models.DecimalField('Сумма по основному требованию (фактически)', max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    sum_amount_penalty_agent_prognosis = models.DecimalField('Сумма неустойки (заявленная)', max_digits=10,decimal_places=2, default=0, blank=True, null=True)
    sum_amount_penalty_agent = models.DecimalField('Сумма неустойки (фактически)', max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    sum_of_penalty_prognosis = models.DecimalField('Сумма штрафа (прогнозируемая)', max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    sum_of_penalty = models.DecimalField('Сумма штрафа (фактически)', max_digits=10, decimal_places=2, default=0,blank=True, null=True)
    sum_amount_moral_damage_prognosis = models.DecimalField('Сумма морального/репутационного вреда (заявленая)',max_digits=10, decimal_places=2, default=0, blank=True,null=True)
    sum_amount_moral_damage = models.DecimalField('Сумма морального/репутационного вреда (фактически)', max_digits=10,decimal_places=2, default=0, blank=True, null=True)
    sum_amount_expertize = models.DecimalField('Сумма экспертизы', max_digits=10, decimal_places=2, default=0,blank=True, null=True)
    sum_amount_expertize_prognosis = models.DecimalField('Сумма экспертизы (заявленная)', max_digits=10,decimal_places=2, default=0, blank=True, null=True)
    total_sum_in_the_case_prognosis = models.DecimalField('Общая заявленная сумма по делу', max_digits=10,decimal_places=2, default=0, blank=True, null=True)
    total_sum_in_the_case = models.DecimalField('Общая присужденная сумма по делу', max_digits=10, decimal_places=2,default=0, blank=True, null=True)

    # Суммы в судебном деле (Юридические услуги)
    total_amount_expected_additional = models.DecimalField('Сумма заявленная за юридические услуги ОБЩАЯ',max_digits=10, decimal_places=2, default=0, blank=True,null=True)
    sum_amount_expected_additional = models.DecimalField('Сумма заявленная за юридические услуги', max_digits=10,decimal_places=2, default=0, blank=True, null=True)
    postage_expected_expenses = models.DecimalField('Сумма заявленная за почтовые расходы', max_digits=10,decimal_places=2, default=0, blank=True, null=True)
    fare_expected_expenses = models.DecimalField('Сумма заявленная за транспортные расходы', max_digits=10,decimal_places=2, default=0, blank=True, null=True)
    other_expected_expenses = models.DecimalField('Иные заявленные расходы', max_digits=10, decimal_places=2, default=0,blank=True, null=True)
    total_amount_additional = models.DecimalField('Сумма взысканная за юр. услуги ОБЩАЯ', max_digits=10,decimal_places=2, default=0, blank=True, null=True)
    sum_amount_additional = models.DecimalField('Сумма взысканная за юр услуги', max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    postage_expenses = models.DecimalField('Сумма взыскананная за почтовые расходы', max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    fare_expenses = models.DecimalField('Сумма присужденная за транспортные расходы', max_digits=10, decimal_places=2,default=0, blank=True, null=True)
    other_expenses = models.DecimalField('Иные присужденные расходы', max_digits=10, decimal_places=2, default=0,blank=True, null=True)

    # Рабочие переменные модели судебного дела
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Создал')
    date_of_judgment = models.DateField('Дата вынесения судебного решения', blank=True, null=True)
    responsible = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Ответственный',related_name='+')
    observer = models.ManyToManyField(User, blank=True, verbose_name='Ответственный', related_name='obs')
    arhive = models.BooleanField('Убрать в архив', blank=True, default=False)
    created_date = models.DateField('Дата создания', blank=True, null=True)
    arhive_date = models.DateField('Дата перевода в архив', blank=True, null=True)
    read_court_users = models.ManyToManyField(User, blank=True, null=True, related_name=" who_read+")
    is_complete = models.BooleanField('Готовый экземпляр судебного дела', default=False)
    date_create_object_model = models.DateTimeField(auto_now_add=True, null=True)
    last_change_make_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,related_name="last_change_make_user+")
    comment_count_model = models.IntegerField(blank=True, null=True, default=None)

    # Тестовые поля модели
    jungment = models.ForeignKey(CourtsJudgment, blank=True, null=True, default=None, on_delete=models.CASCADE)


    # сохранение даты вынесения судебного решения
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.was_court_result = self.court_result

    # сохранение даты вынесения судебного решения
    def save(self, *args, **kwargs):
        if self.court_result and not self.was_court_result:
            self.date_of_judgment = timezone.now()
        return super().save(*args, **kwargs)
     
    def __str__(self):
        return "%s против %s" % (self.plaintiff, self.defendant)

class CommentsCourts(models.Model):
    article = models.ForeignKey(Courts, on_delete = models.CASCADE, verbose_name='Судебное дело', blank = True, null = True,related_name='comments_articles' )
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Автор комментария', null = True)
    create_date = models.DateTimeField(auto_now_add = True, null = True)
    text = models.TextField(verbose_name='Текст комментария')



    def __str__(self):
        return self.text
        
class CourtDocuments(models.Model):
    court_ducuments = models.FileField(upload_to = 'Courtdocuments/')
    article = models.ForeignKey(Courts, on_delete = models.CASCADE, verbose_name='Судебное дело', blank = True, null = True, related_name='documents')


    def save(self, *args, **kwargs):
        try:
            this_record = CourtDocuments.objects.get(id=self.id)
            if this_record.court_ducuments != self.court_ducuments:
                this_record.court_ducuments.delete(save=False)
        except:
            pass
        super(CourtDocuments, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.court_ducuments.delete(save=False)
        super(CourtDocuments, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.court_ducuments)

class CourtJudgment(models.Model):
    court_judjment = models.FileField(upload_to = 'Courtjudgment/')
    article = models.ForeignKey(Courts, on_delete = models.CASCADE, verbose_name='Судебное дело', blank = True, null = True, related_name='judgment')

    def save(self, *args, **kwargs):
        try:
            this_record = CourtJudgment.objects.get(id=self.id)
            if this_record.court_judjment != self.court_judjment:
                this_record.court_judjment.delete(save=False)
        except:
            pass
        super(CourtJudgment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.court_judjment.delete(save=False)
        super(CourtJudgment, self).delete(*args, **kwargs)


    def __str__(self):
        return str(self.court_judjment)