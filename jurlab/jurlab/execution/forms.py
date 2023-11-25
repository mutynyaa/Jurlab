from django import forms
from .models import *
from django.forms import ModelForm
from profiles.models import Profiles
from django.forms import ClearableFileInput
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from courts.forms import DateInput



class NewExecutionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewExecutionForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['observer'].choices = [(user.pk, '%s %s %s.' % (user.profiles.surname, user.profiles.name, user.profiles.fathers_name[0:1])) for user in users]
    class Meta:
        model = Executions
        fields = ('dispath_document', 'observer', 'document_nmb', 'document_date', 'agency', 'agency_address', 'agency_phone', 'debt', 'exact', 'executor', 'text', 'arhive', 'category',)
        widgets = {
            'observer': forms.SelectMultiple(attrs={'class': 'choise_observer_block'}),
            'category': forms.Select(attrs={'class': 'choise_category_block'}),
            'instance': forms.Select(attrs={'class': 'choise_instance_block'}),
            'text': forms.Textarea(attrs={'class': 'choise_text_block'}),
            'document_date': DateInput(),
            'dispath_document': DateInput(),
        }

class RedactExecutionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RedactExecutionForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['observer'].choices = [(user.pk, '%s %s %s.' % (user.profiles.surname, user.profiles.name, user.profiles.fathers_name[0:1])) for user in users]
        self.fields['responsible'].choices = [(user.pk, '%s %s %s.' % (user.profiles.surname, user.profiles.name, user.profiles.fathers_name[0:1])) for user in users]
    class Meta:
        model = Executions
        fields = ('responsible', 'dispath_document', 'observer', 'document_nmb', 'document_date', 'agency', 'agency_address', 'agency_phone', 'debt', 'exact', 'executor', 'text', 'arhive', 'category',)
        widgets = {
            'observer': forms.SelectMultiple(attrs={'class': 'choise_observer_block'}),
            'category': forms.Select(attrs={'class': 'choise_category_block'}),
            'instance': forms.Select(attrs={'class': 'choise_instanse_block'}),
            'text': forms.Textarea(attrs={'class': 'choise_text_block'}),
            'document_date': DateInput(),
            'dispath_document': DateInput(),
        }
       
        
class ExCommentForm(ModelForm):
    class Meta:
        model = ExecutionComments
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'comment_input_form','placeholder': 'Введите ваш комментарий'}),
            'text': SummernoteWidget()
        }
        
        
class ExDocumentForm(ModelForm):

    class Meta:
        model = ExecutionDocuments
        fields = ('execution_ducuments',)
        widgets = {
            'execution_ducuments': ClearableFileInput(attrs={'multiple': False,'class':'court_document_input'}),
        }
        
        
class CategoryFilterForm(ModelForm):
    min_dept_summ = forms.IntegerField(label="От", required=False)
    max_dept_summ = forms.IntegerField(label="До", required=False)
    only_my_execution = forms.BooleanField(label="Только мои исполнительные производства", required=False)

    class Meta:
        model = Executions
        fields = ('category', )
        widgets = {
            'category': forms.Select(attrs={'class': 'choise_category_block'}),
        }

class ExSearchForm(ModelForm):
    text = forms.CharField(label="Поиск", required=False)