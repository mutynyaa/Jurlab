from django.db import models
from django.contrib.auth.models import User
from courts.models import Courts
from profiles.models import Profiles
from simple_history.models import HistoricalRecords

class ExecutionCategory(models.Model):
    ex_category = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.ex_category


class Executions(models.Model):
    court = models.ForeignKey(Courts, blank=True, null=True, on_delete=models.CASCADE, verbose_name = 'Суд')
    category = models.ForeignKey(ExecutionCategory, blank=True, null=True, default=None, on_delete=models.CASCADE)
    created_date = models.DateField(blank=True, null = True, auto_now_add=True)
    dispath_document = models.DateField(blank=True, null = True)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name = 'Создал')
    responsible = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Ответственный', related_name ='+')
    observer = models.ManyToManyField(User, verbose_name='Наблюдатель', related_name ='observer')
    arhive = models.BooleanField('Убрать в архив', blank=True, default=False)
    document_nmb = models.CharField('№ исполнительного листа', max_length = 200,blank=True, null=True, default="")
    document_date = models.DateField(blank=True, null = True)
    agency = models.CharField('Наименование органа исполнения', max_length = 200,blank=True, null=True, default="")
    agency_address = models.CharField('Адрес (местонахождение) органа исполнения', max_length = 200, blank=True, null=True, default=None)
    agency_phone = models.CharField('Контактный телефон', max_length = 200, blank=True, null=True, default=None)
    debt = models.DecimalField('Сумма долга', max_digits=10, decimal_places=2, default=0)
    exact = models.DecimalField('Взыскано', max_digits=10, decimal_places=2, default=0)
    executor = models.CharField('ФИО судебного пристава-исполнителя', max_length = 200, blank=True, null=True, default=None)
    text = models.TextField('Дополнительная информация', default=" ")
    execution_count_model = models.IntegerField(blank=True, null=True, default=None)
    history = HistoricalRecords(cascade_delete_history=True)
    last_change_make_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="last_change_make_user+")
    read_execution_users = models.ManyToManyField(User, blank=True, null=True, related_name=" who_read+")

     
    def __str__(self):
        return "%s | %s" % (self.id, self.court)
        
        
class ExecutionComments(models.Model):
    article = models.ForeignKey(Executions, on_delete = models.CASCADE, verbose_name='Исполнительное производство', blank = True, null = True,related_name='comments_articles_ex' )
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Автор комментария', null = True)
    create_date = models.DateTimeField(auto_now_add = True, null = True)
    text = models.TextField(verbose_name='Текст комментария')

    def __str__(self):
        return self.text
        
class ExecutionDocuments(models.Model):
    execution_ducuments = models.FileField(upload_to = 'Executiondocuments/')
    article = models.ForeignKey(Executions, on_delete = models.CASCADE, verbose_name='Исполнительное производство', blank = True, null = True, related_name='documents')

    def save(self, *args, **kwargs):
        try:
            this_record = ExecutionDocuments.objects.get(id=self.id)
            if this_record.execution_ducuments != self.execution_ducuments:
                this_record.execution_ducuments.delete(save=False)
        except:
            pass
        super(ExecutionDocuments, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.execution_ducuments.delete(save=False)
        super(ExecutionDocuments, self).delete(*args, **kwargs)


    def __str__(self):
        return str(self.execution_ducuments)