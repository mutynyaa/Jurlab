from django import forms
from .models import *
from django.forms import ModelForm
from profiles.models import Profiles
from courts.models import Courts
import datetime
from django.utils import timezone


class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


# Форма выбора даты в периоде
class MonthYearAllStatisticsFilter(forms.Form):
    from_year_month = forms.DateField(label="От", required=True, widget=DateInput())
    to_year_month = forms.DateField(label="До", required=True, widget=DateInput())


# Форма выбора пользователя и даты
class ChoiceUserAndDateFilter(ModelForm):
    from_year_month = forms.DateField(label="От", required=True, widget=DateInput())
    to_year_month = forms.DateField(label="До", required=True, widget=DateInput())

    def __init__(self, *args, **kwargs):
        super(ChoiceUserAndDateFilter, self).__init__(*args, **kwargs)
        users = User.objects.all()
        self.fields['responsible'].choices = [(user.pk, '%s %s %s.' % (user.profiles.surname, user.profiles.name, user.profiles.fathers_name[0:1])) for user in users]


    class Meta:
        model = Courts
        fields = ('responsible',)

