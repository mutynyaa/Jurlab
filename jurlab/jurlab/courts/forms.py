from django import forms
from .models import *
from django.forms import ModelForm
from profiles.models import Profiles
from django.forms import ClearableFileInput
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
import datetime

class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)

class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)

class CourtsFormRedact(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourtsFormRedact, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['observer'].choices = [(user.pk, '%s %s %s.' % (user.profiles.surname, user.profiles.name, user.profiles.fathers_name[0:1])) for user in users]
        self.fields['responsible'].choices = [(user.pk, '%s %s %s.' % (user.profiles.surname, user.profiles.name, user.profiles.fathers_name[0:1])) for user in users]

    class Meta:
        model = Courts
        fields = ('responsible', 'arhive', 'instance', 'status', 'jurisdiction', 'category',
                  'sum_amount_expected_additional', 'sum_amount_additional',
                  'sum_amount_expertize', 'sum_amount_moral_damage', 'sum_amount_main', 'sum_amount_moral_damage',
                  'court_result', 'history_court_hearing', 'actual_court_hearing', 'plaintiff', 'defendant',
                  'court_phone', 'court_address', 'date_getting_lawsuit', 'case_number','court_name','plaintiff',
                  'defendant','text', 'observer', 'sum_amount_penalty_agent','sum_amount_main_prognosis',
                  'sum_amount_penalty_agent_prognosis', 'sum_of_penalty_prognosis', 'sum_of_penalty',
                  'sum_amount_moral_damage_prognosis', 'defendant_representative',
                  'plaintiff_representative', 'third_persons', 'type_proceedings_choises',
                  'state_duty', 'state_duty_prognosis', 'sum_amount_expertize_prognosis',
                  'sum_amount_expected_additional','postage_expected_expenses','fare_expected_expenses','other_expected_expenses',
                  'sum_amount_additional','postage_expenses','fare_expenses', 'other_expenses', 'type_of_decision_civil',
                  'type_of_decision_criminal',
                  )
        widgets = {
            'observer': forms.SelectMultiple(attrs={'class': 'choise_observer_block'}),
            'category': forms.Select(attrs={'class': 'choise_category_block'}),
            'responsible': forms.Select(attrs={'class': 'choise_responsible_block'}),
            'instance': forms.Select(attrs={'class': 'choise_instanse_block'}),
            'status': forms.Select(attrs={'class': 'choise_status_block'}),
            'jurisdiction': forms.Select(attrs={'class': 'choise_jurisdiction_block'}),
            'type_proceedings_choises': forms.Select(attrs={'class': 'choise_type_proceedings_block'}),
            'text': forms.Textarea(attrs={'class': 'choise_text_block'}),
            'history_court_hearing': forms.Textarea(attrs={'class': 'choise_history_court_hearing_block'}),
            'court_result': forms.Select(attrs={'class': 'choise_court_result_block'}),
            'date_getting_lawsuit': DateInput(),
            'actual_court_hearing': DateTimeInput(),

            
        }
        labels = {
            'observer': ('my name'),
        }

class CourtsFormNew(forms.ModelForm):

    class Meta:
        model = Courts
        fields = ('type_proceedings_choises',)
            



class CommentForm(ModelForm):
    class Meta:
        model = CommentsCourts
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'comment_input_form','placeholder': 'Введите ваш комментарий'}),
            'text': SummernoteWidget()
        }
        
class DocumentForm(ModelForm):

    class Meta:
        model = CourtDocuments
        fields = ('court_ducuments',)
        widgets = {
            'court_ducuments': ClearableFileInput(attrs={'multiple': False,}),
        }

class JudgmentForm(ModelForm):

    class Meta:
        model = CourtJudgment
        fields = ('court_judjment',)
        widgets = {
            'court_judjment': ClearableFileInput(attrs={'multiple': False}),
        }

     
class FilterForm(ModelForm):

    class Meta:
        model = Profiles
        fields = ('only_their_courts', 'courts_common_jurisdiction', )


class CategoryFilterForm(ModelForm):
    min_claim_summ = forms.IntegerField(label="От", required=False)
    max_claim_summ = forms.IntegerField(label="До", required=False)
    only_my_courts = forms.BooleanField(label="Только мои суды", required=False)
    only_unread_courts = forms.BooleanField(label="Только непрочитанные", required=False)

    class Meta:
        model = Courts
        fields = ('instance', 'status', 'jurisdiction', 'category', 'type_proceedings_choises', 'court_result', )
        widgets = {
            'instance': forms.Select(attrs={'class': 'choise_instanse_block'}),
            'status': forms.Select(attrs={'class': 'choise_status_block'}),
            'jurisdiction': forms.Select(attrs={'class': 'choise_jurisdiction_block'}),
            'type_proceedings_choises': forms.Select(attrs={'class': 'choise_type_proceedings_block',}),
            'category': forms.Select(attrs={'class': 'choise_category_block'}),
        }



class CourtSearchForm(ModelForm):
    text = forms.CharField(label="Поиск", required=False)

class DeleteCommentForm(ModelForm):

    class Meta:
        model = CommentsCourts
        fields = ()


class CourtsFormNewStepTwo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourtsFormNewStepTwo, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['observer'].choices = [(user.pk, '%s %s %s.' % (user.profiles.surname, user.profiles.name, user.profiles.fathers_name[0:1])) for user in users]
        self.fields['responsible'].choices = [(user.pk, '%s %s %s.' % (user.profiles.surname, user.profiles.name, user.profiles.fathers_name[0:1])) for user in users]

    class Meta:
        model = Courts
        fields = (
                  'responsible', 'instance', 'status',
                  'jurisdiction', 'category',  'sum_amount_expected_additional',
                  'actual_court_hearing', 'court_phone', 'court_address',
                  'date_getting_lawsuit', 'case_number','court_name','text', 'observer', 'sum_amount_main_prognosis',
                  'sum_amount_penalty_agent_prognosis', 'sum_of_penalty_prognosis',
                  'sum_amount_moral_damage_prognosis', 'defendant_representative',
                  'plaintiff_representative', 'third_persons', 'plaintiff', 'defendant',
                  'state_duty_prognosis', 'sum_amount_expertize_prognosis'

                  )

        widgets = {
            'observer': forms.SelectMultiple(attrs={'class': 'choise_observer_block'}),
            'category': forms.Select(attrs={'class': 'choise_category_block'}),
            'responsible': forms.Select(attrs={'class': 'choise_responsible_block'}),
            'instance': forms.Select(attrs={'class': 'choise_instanse_block'}),
            'status': forms.Select(attrs={'class': 'choise_status_block'}),
            'jurisdiction': forms.Select(attrs={'class': 'choise_jurisdiction_block'}),

            'text': forms.Textarea(attrs={'class': 'choise_text_block'}),
            'history_court_hearing': forms.Textarea(attrs={'class': 'choise_history_court_hearing_block'}),
            'court_result': forms.NullBooleanSelect(attrs={'class': 'choise_court_result_block'}),
            'date_getting_lawsuit': DateInput(),
            'actual_court_hearing': DateTimeInput(),
        }