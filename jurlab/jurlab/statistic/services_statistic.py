from django.shortcuts import render
from courts.models import Courts
from execution.models import Executions
from django.db.models import Sum
from django.contrib.auth.decorators import permission_required
from execution.models import Executions
from django.core.exceptions import ObjectDoesNotExist
from mainpage.models import Supervisor
from django.db.models import Q
from .forms import MonthYearAllStatisticsFilter, ChoiceUserAndDateFilter

# Логика статистики "все судебные дела"
def all_court_statistics_logic(request):
    # Все судебные дела
    all_courts = Courts.objects.filter(is_complete=True).count()
    # Все выйгранные судебные дела
    all_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(court_result=1)).count()
    # Все проигранные судебные дела
    all_courts_defeat = Courts.objects.filter(Q(is_complete=True) & Q(court_result=2)).count()
    # Все активные судебные дела
    all_active_courts = Courts.objects.filter(Q(is_complete=True) & Q(arhive=False)).count()
    # Все судебные дела в архиве
    all_courts_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True)).count()
    # Все судебные дела кроме дел без решения
    only_win_or_defeat_courts = all_courts_win + all_courts_defeat
    # Соотношение выйгранных судебных дел к проигранным в процентах
    try:
        all_courts_result_win_percent = all_courts_win / only_win_or_defeat_courts * 100
    except ZeroDivisionError:
        all_courts_result_win_percent = None
    # Соотношение проигранных судебных дел к выйгранным в процентах
    try:
        all_courts_result_defeat_percent = all_courts_defeat / only_win_or_defeat_courts * 100
    except ZeroDivisionError:
        all_courts_result_defeat_percent = None
    # Применение диапозона дат к статистическим данным с помощью формы
    month_year_filter = MonthYearAllStatisticsFilter(request.GET)
    if month_year_filter.is_valid():
        # перезаписываем все данные с фильтром
        # все суды, дата создания которых входит в дипозон фильтра
        all_courts = Courts.objects.filter(Q(created_date__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"])) & Q(is_complete=True)).count()
        # все выйгранные суды, дата вынесения судебного решения которых входит в дипозон фильтра
        all_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(court_result=1) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # все проигранные суды, дата вынесения судебного решения которых входит в дипозон фильтра
        all_courts_defeat = Courts.objects.filter(Q(is_complete=True) & Q(court_result=2) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # Все активные судебные дела
        all_active_courts = Courts.objects.filter(Q(created_date__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"])) & Q(is_complete=True) & Q(arhive=False)).count()
        # Все судебные дела в архиве
        all_courts_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(arhive_date__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # сумма проигранных и выйгранных судов в диапозоне фильтра
        only_win_or_defeat_courts = all_courts_win + all_courts_defeat
        try:
            all_courts_result_win_percent = all_courts_win / only_win_or_defeat_courts * 100
        except ZeroDivisionError:
            all_courts_result_win_percent = None
        try:
            all_courts_result_defeat_percent = all_courts_defeat / only_win_or_defeat_courts * 100
        except ZeroDivisionError:
            all_courts_result_defeat_percent = None


    return all_courts, all_courts_win, all_courts_defeat, all_courts_result_win_percent, \
           all_courts_result_defeat_percent, month_year_filter, all_active_courts, all_courts_in_archive



# Логика статистики "гражданские дела"
def civil_court_statistics_logic(request):
    # Все гражданские дела
    all_civil_courts = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=1)).count()
    # Все выйгранные гражданские дела
    all_civil_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=1) & Q(court_result=1)).count()
    # Все проигранные гражданские дела
    all_civil_courts_defeat = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=1) & Q(court_result=2)).count()
    # активные гражданские судебные дела
    all_active_civil_courts = Courts.objects.filter(Q(is_complete=True) & Q(arhive=False) & Q(type_proceedings_choises=1)).count()
    # Все гражданские судебные дела в архиве
    all_civil_courts_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(type_proceedings_choises=1)).count()
    # Все гражданские дела кроме дел без решения
    only_win_or_defeat_civil_courts = all_civil_courts_win + all_civil_courts_defeat
    # Соотношение выйгранных гражданских дел к проигранным в процентах
    try:
        all_civil_courts_result_win_percent = all_civil_courts_win / only_win_or_defeat_civil_courts * 100
    except ZeroDivisionError:
        all_civil_courts_result_win_percent = None
    # Соотношение проигранных гражданских дел к выйгранным в процентах
    try:
        all_civil_courts_result_defeat_percent = all_civil_courts_defeat / only_win_or_defeat_civil_courts * 100
    except ZeroDivisionError:
        all_civil_courts_result_defeat_percent = None

    # Применение диапозона дат к статистическим данным с помощью формы
    month_year_filter = MonthYearAllStatisticsFilter(request.GET)
    if month_year_filter.is_valid():
        # перезаписываем все данные с фильтром
        # все гражданские суды, дата создания которых входит в дипозон фильтра
        all_civil_courts = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=1) & Q(created_date__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # все гражданские выйгранные суды, дата вынесения судебного решения которых входит в дипозон фильтра
        all_civil_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=1) & Q(court_result=1) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # все проигранные гражданские суды, дата вынесения судебного решения которых входит в дипозон фильтра
        all_civil_courts_defeat = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=1) & Q(court_result=2) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # Все активные судебные дела
        all_active_civil_courts = Courts.objects.filter(Q(created_date__range=(
            month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"])) & Q(
            is_complete=True) & Q(arhive=False) & Q(type_proceedings_choises=1)).count()
        # Все судебные дела в архиве
        all_civil_courts_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(arhive_date__range=(
            month_year_filter.cleaned_data["from_year_month"],
            month_year_filter.cleaned_data["to_year_month"])) & Q(type_proceedings_choises=1)).count()
        # сумма проигранных и выйгранных гражданских судов в диапозоне фильтра
        only_win_or_defeat_civil_courts = all_civil_courts_win + all_civil_courts_defeat
        try:
            all_civil_courts_result_win_percent = all_civil_courts_win / only_win_or_defeat_civil_courts * 100
        except ZeroDivisionError:
            all_civil_courts_result_win_percent = None
        try:
            all_civil_courts_result_defeat_percent = all_civil_courts_defeat / only_win_or_defeat_civil_courts * 100
        except ZeroDivisionError:
            all_civil_courts_result_defeat_percent = None

    return all_civil_courts, all_civil_courts_win, all_civil_courts_defeat,\
        all_civil_courts_result_win_percent, all_civil_courts_result_defeat_percent, all_active_civil_courts,\
        all_civil_courts_in_archive


# Логика статистики "уголовные дела"
def criminal_court_statistics_logic(request):
    # Все уголовные дела
    all_criminal_courts = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=2)).count()
    # Все выйгранные уголовные дела
    all_criminal_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=2) & Q(court_result=1)).count()
    # Все проигранные уголовные дела
    all_criminal_courts_defeat = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=2) & Q(court_result=2)).count()
    # активные уголовные судебные дела
    all_active_criminal_courts = Courts.objects.filter(Q(is_complete=True) & Q(arhive=False) & Q(type_proceedings_choises=2)).count()
    # Все уголовные судебные дела в архиве
    all_criminal_courts_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(type_proceedings_choises=2)).count()
    # Все уголовные дела кроме дел без решения
    only_win_or_defeat_criminal_courts = all_criminal_courts_win + all_criminal_courts_defeat
    # Соотношение выйгранных уголовных дел к проигранным в процентах
    try:
        all_criminal_courts_result_win_percent = all_criminal_courts_win / only_win_or_defeat_criminal_courts * 100
    except ZeroDivisionError:
        all_criminal_courts_result_win_percent = None
    # Соотношение проигранных уголовных дел к выйгранным в процентах
    try:
        all_criminal_courts_result_defeat_percent = all_criminal_courts_defeat / only_win_or_defeat_criminal_courts * 100
    except ZeroDivisionError:
        all_criminal_courts_result_defeat_percent = None

    # Применение диапозона дат к статистическим данным с помощью формы
    month_year_filter = MonthYearAllStatisticsFilter(request.GET)
    if month_year_filter.is_valid():
        # перезаписываем все данные с фильтром
        # все уголовные суды, дата создания которых входит в дипозон фильтра
        all_criminal_courts = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=2) & Q(created_date__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # все уголовные выйгранные суды, дата вынесения судебного решения которых входит в дипозон фильтра
        all_criminal_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=2) & Q(court_result=1) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # все проигранные уголовные суды, дата вынесения судебного решения которых входит в дипозон фильтра
        all_criminal_courts_defeat = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=2) & Q(court_result=2) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # Все активные уголовные судебные дела
        all_active_criminal_courts = Courts.objects.filter(Q(created_date__range=(
            month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"])) & Q(
            is_complete=True) & Q(arhive=False) & Q(type_proceedings_choises=2)).count()
        # Все уголовные судебные дела в архиве
        all_criminal_courts_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(arhive_date__range=(
            month_year_filter.cleaned_data["from_year_month"],
            month_year_filter.cleaned_data["to_year_month"])) & Q(type_proceedings_choises=2)).count()
        # сумма проигранных и выйгранных уголовные судов в диапозоне фильтра
        only_win_or_defeat_criminal_courts = all_criminal_courts_win + all_criminal_courts_defeat
        try:
            all_criminal_courts_result_win_percent = all_criminal_courts_win / only_win_or_defeat_criminal_courts * 100
        except ZeroDivisionError:
            all_criminal_courts_result_win_percent = None
        try:
            all_criminal_courts_result_defeat_percent = all_criminal_courts_defeat / only_win_or_defeat_criminal_courts * 100
        except ZeroDivisionError:
            all_criminal_courts_result_defeat_percent = None

    return all_criminal_courts, all_criminal_courts_win, all_criminal_courts_defeat,\
        all_criminal_courts_result_win_percent, all_criminal_courts_result_defeat_percent, all_active_criminal_courts,\
        all_criminal_courts_in_archive


# Логика статистики "Административные дела (КАС)"
def administrical_proceedings_court_statistics_logic(request):
    # Все дела КАС
    all_administrical_proceedings_courts = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=3)).count()
    # Все выйгранные дела КАС
    all_administrical_proceedings_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=3) & Q(court_result=1)).count()
    # Все проигранные дела КАС
    all_administrical_proceedings_courts_defeat = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=3) & Q(court_result=2)).count()
    # активные дела КАС
    all_active_administrical_proceedings_courts = Courts.objects.filter(Q(is_complete=True) & Q(arhive=False) & Q(type_proceedings_choises=3)).count()
    # Все дела КАС в архиве
    all_administrical_proceedings_courts_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(type_proceedings_choises=3)).count()
    # Все дела КАС кроме дел без решения
    only_win_or_defeat_administrical_proceedings_courts = all_administrical_proceedings_courts_win + all_administrical_proceedings_courts_defeat
    # Соотношение выйгранных дел КАС к проигранным в процентах
    try:
        all_administrical_proceedings_courts_result_win_percent = all_administrical_proceedings_courts_win / only_win_or_defeat_administrical_proceedings_courts * 100
    except ZeroDivisionError:
        all_administrical_proceedings_courts_result_win_percent = None
    # Соотношение проигранных дел КАС к выйгранным в процентах
    try:
        all_administrical_proceedings_courts_result_defeat_percent = all_administrical_proceedings_courts_defeat / only_win_or_defeat_administrical_proceedings_courts * 100
    except ZeroDivisionError:
        all_administrical_proceedings_courts_result_defeat_percent = None

    # Применение диапозона дат к статистическим данным с помощью формы
    month_year_filter = MonthYearAllStatisticsFilter(request.GET)
    if month_year_filter.is_valid():
        # перезаписываем все данные с фильтром
        # все дела КАС, дата создания которых входит в дипозон фильтра
        all_administrical_proceedings_courts = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=3) & Q(created_date__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # все дела КАС выйгранные, дата вынесения судебного решения которых входит в дипозон фильтра
        all_administrical_proceedings_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=3) & Q(court_result=1) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # все проигранные дела КАС, дата вынесения судебного решения которых входит в дипозон фильтра
        all_administrical_proceedings_courts_defeat = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=3) & Q(court_result=2) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # Все активные дела КАС
        all_active_administrical_proceedings_courts = Courts.objects.filter(Q(created_date__range=(
            month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"])) & Q(
            is_complete=True) & Q(arhive=False) & Q(type_proceedings_choises=3)).count()
        # Все дела КАС в архиве
        all_administrical_proceedings_courts_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(arhive_date__range=(
            month_year_filter.cleaned_data["from_year_month"],
            month_year_filter.cleaned_data["to_year_month"])) & Q(type_proceedings_choises=3)).count()
        # сумма проигранных и выйгранных дел КАС в диапозоне фильтра
        only_win_or_defeat_administrical_proceedings_courts = all_administrical_proceedings_courts_win + all_administrical_proceedings_courts_defeat
        try:
            all_administrical_proceedings_courts_result_win_percent = all_administrical_proceedings_courts_win / only_win_or_defeat_administrical_proceedings_courts * 100
        except ZeroDivisionError:
            all_administrical_proceedings_courts_result_win_percent = None
        try:
            all_administrical_proceedings_courts_result_defeat_percent = all_administrical_proceedings_courts_defeat / only_win_or_defeat_administrical_proceedings_courts * 100
        except ZeroDivisionError:
            all_administrical_proceedings_courts_result_defeat_percent = None

    return all_administrical_proceedings_courts, all_administrical_proceedings_courts_win, all_administrical_proceedings_courts_defeat,\
        all_administrical_proceedings_courts_result_win_percent, all_administrical_proceedings_courts_result_defeat_percent, all_active_administrical_proceedings_courts,\
        all_administrical_proceedings_courts_in_archive


# Логика статистики "Административные дела (КоАП)"
def administrical_offence_court_statistics_logic(request):
    # Все дела КоАП
    all_administrical_offence_courts = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=4)).count()
    # Все выйгранные дела КоАП
    all_administrical_offence_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=4) & Q(court_result=1)).count()
    # Все проигранные дела КоАП
    all_administrical_offence_courts_defeat = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=4) & Q(court_result=2)).count()
    # активные дела КоАП
    all_active_administrical_offence_courts = Courts.objects.filter(Q(is_complete=True) & Q(arhive=False) & Q(type_proceedings_choises=4)).count()
    # Все дела КоАП в архиве
    all_administrical_offence_courts_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(type_proceedings_choises=4)).count()
    # Все дела КоАП кроме дел без решения
    only_win_or_defeat_administrical_offence_courts = all_administrical_offence_courts_win + all_administrical_offence_courts_defeat
    # Соотношение выйгранных дел КоАП к проигранным в процентах
    try:
        all_administrical_offence_courts_result_win_percent = all_administrical_offence_courts_win / only_win_or_defeat_administrical_offence_courts * 100
    except ZeroDivisionError:
        all_administrical_offence_courts_result_win_percent = None
    # Соотношение проигранных дел КоАП к выйгранным в процентах
    try:
        all_administrical_offence_courts_result_defeat_percent = all_administrical_offence_courts_defeat / only_win_or_defeat_administrical_offence_courts * 100
    except ZeroDivisionError:
        all_administrical_offence_courts_result_defeat_percent = None

    # Применение диапозона дат к статистическим данным с помощью формы
    month_year_filter = MonthYearAllStatisticsFilter(request.GET)
    if month_year_filter.is_valid():
        # перезаписываем все данные с фильтром
        # все дела КоАП, дата создания которых входит в дипозон фильтра
        all_administrical_offence_courts = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=4) & Q(created_date__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # все дела КоАП выйгранные, дата вынесения судебного решения которых входит в дипозон фильтра
        all_administrical_offence_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=4) & Q(court_result=1) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # все проигранные дела КоАП, дата вынесения судебного решения которых входит в дипозон фильтра
        all_administrical_offence_courts_defeat = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=4) & Q(court_result=2) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # Все активные дела КоАП
        all_active_administrical_offence_courts = Courts.objects.filter(Q(created_date__range=(
            month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"])) & Q(
            is_complete=True) & Q(arhive=False) & Q(type_proceedings_choises=4)).count()
        # Все дела КоАП в архиве
        all_administrical_offence_courts_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(arhive_date__range=(
            month_year_filter.cleaned_data["from_year_month"],
            month_year_filter.cleaned_data["to_year_month"])) & Q(type_proceedings_choises=4)).count()
        # сумма проигранных и выйгранных дел КоАП в диапозоне фильтра
        only_win_or_defeat_administrical_offence_courts = all_administrical_offence_courts_win + all_administrical_offence_courts_defeat
        try:
            all_administrical_offence_courts_result_win_percent = all_administrical_offence_courts_win / only_win_or_defeat_administrical_offence_courts * 100
        except ZeroDivisionError:
            all_administrical_offence_courts_result_win_percent = None
        try:
            all_administrical_offence_courts_result_defeat_percent = all_administrical_offence_courts_defeat / only_win_or_defeat_administrical_offence_courts * 100
        except ZeroDivisionError:
            all_administrical_offence_courts_result_defeat_percent = None

    return all_administrical_offence_courts, all_administrical_offence_courts_win, all_administrical_offence_courts_defeat,\
        all_administrical_offence_courts_result_win_percent, all_administrical_offence_courts_result_defeat_percent, all_active_administrical_offence_courts,\
        all_administrical_offence_courts_in_archive


# Логика статистики "Личная статистика"
# действующая нагрузка сотрудника
def personal_court_statistic_load(request):
    # все активные судебные дела, за которые сотрудник ответственнен
    all_active_personal_courts = Courts.objects.filter(Q(is_complete=True) & Q(arhive=False) & Q(responsible=request.user)).count()
    # гражданские активные судебные дела, за которые сотрудник ответственнен
    all_active_personal_courts_civil = Courts.objects.filter(Q(is_complete=True) & Q(arhive=False) & Q(responsible=request.user) & Q(type_proceedings_choises=1)).count()
    # уголовные активные судебные дела, за которые сотрудник ответственнен
    all_active_personal_courts_criminal = Courts.objects.filter(Q(is_complete=True) & Q(arhive=False) & Q(responsible=request.user) & Q(type_proceedings_choises=2)).count()
    # административные (КАС) активные судебные дела, за которые сотрудник ответственнен
    all_active_personal_courts_administrical_proceedings = Courts.objects.filter(Q(is_complete=True) & Q(arhive=False) & Q(responsible=request.user) & Q(type_proceedings_choises=3)).count()
    # административные (КоАП) активные судебные дела, за которые сотрудник ответственнен
    all_active_personal_courts_administrical_offence = Courts.objects.filter(Q(is_complete=True) & Q(arhive=False) & Q(responsible=request.user) & Q(type_proceedings_choises=4)).count()

    return all_active_personal_courts, all_active_personal_courts_civil, all_active_personal_courts_criminal, all_active_personal_courts_administrical_proceedings, \
    all_active_personal_courts_administrical_offence

# Архив сотрудника (все дела)
def personal_court_statistic_archive(request):
    all_personal_courts_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(responsible=request.user)).count()
    # гражданские судебные дела, за которые сотрудник ответственнен в архиве
    all_personal_courts_civil_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(responsible=request.user) & Q(type_proceedings_choises=1)).count()
    # уголовные судебные дела, за которые сотрудник ответственнен в архиве
    all_personal_courts_criminal_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(responsible=request.user) & Q(type_proceedings_choises=2)).count()
    # административные (КАС) судебные дела, за которые сотрудник ответственнен в архиве
    all_personal_courts_administrical_proceedings_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(responsible=request.user) & Q(type_proceedings_choises=3)).count()
    # административные (КоАП) судебные дела, за которые сотрудник ответственнен в архиве
    all_personal_courts_administrical_offence_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(responsible=request.user) & Q(type_proceedings_choises=4)).count()

    return all_personal_courts_in_archive, all_personal_courts_civil_in_archive, all_personal_courts_criminal_in_archive,all_personal_courts_administrical_proceedings_in_archive, \
           all_personal_courts_administrical_offence_in_archive


# статистика побед и поражений сотрудника
def personal_court_statistic_win_and_defeat(request):
    # проверка на использование формы
    use_form_check = False
    # Все выйгранные дела сотрудника
    all_personal_courts_win= Courts.objects.filter(Q(is_complete=True) & Q(responsible=request.user) & Q(court_result=1)).count()

    # Все выйгранные гражданские дела сотрудника
    civil_personal_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=1) & Q(court_result=1) & Q(responsible=request.user)).count()
    # Все выйгранные уголовные дела сотрудника
    criminal_personal_courts_win= Courts.objects.filter(Q(is_complete=True) & Q(type_proceedings_choises=2) & Q(court_result=1) & Q(responsible=request.user)).count()
    # Все выйгранные дела (КАС) сотрудника
    administrical_proceedings_personal_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(court_result=1) & Q(type_proceedings_choises=3) & Q(responsible=request.user)).count()
    # Все выйгранные дела (КоАП) сотрудника
    administrical_offence_personal_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(court_result=1) & Q(type_proceedings_choises=4) & Q(responsible=request.user)).count()

    # Все проигранные дела сотрудника
    all_personal_courts_defeat = Courts.objects.filter(
        Q(is_complete=True) & Q(responsible=request.user) & Q(court_result=2)).count()

    # Все проигранные гражданские дела сотрудника
    civil_personal_courts_defeat = Courts.objects.filter(
        Q(is_complete=True) & Q(type_proceedings_choises=1) & Q(court_result=2) & Q(responsible=request.user)).count()
    # Все проигранные уголовные дела сотрудника
    criminal_personal_courts_defeat = Courts.objects.filter(
        Q(is_complete=True) & Q(type_proceedings_choises=2) & Q(court_result=2) & Q(responsible=request.user)).count()
    # Все проигранные дела (КАС) сотрудника
    administrical_proceedings_personal_courts_defeat = Courts.objects.filter(
        Q(is_complete=True) & Q(court_result=2) & Q(type_proceedings_choises=3) & Q(responsible=request.user)).count()
    # Все проигранные дела (КоАП) сотрудника
    administrical_offence_personal_courts_defeat = Courts.objects.filter(
        Q(is_complete=True) & Q(court_result=2) & Q(type_proceedings_choises=4) & Q(responsible=request.user)).count()

    only_win_or_defeat_all_courts = all_personal_courts_win + all_personal_courts_defeat
    only_win_or_defeat_civil = civil_personal_courts_win + civil_personal_courts_defeat
    only_win_or_defeat_criminal = criminal_personal_courts_win + criminal_personal_courts_defeat
    only_win_or_defeat_administrical_proceedings = administrical_proceedings_personal_courts_win + administrical_proceedings_personal_courts_defeat
    only_win_or_defeat_administrical_offence = administrical_offence_personal_courts_win + administrical_offence_personal_courts_defeat

    try:
        personal_all_courts_result_win_percent = all_personal_courts_win / only_win_or_defeat_all_courts * 100
    except ZeroDivisionError:
        personal_all_courts_result_win_percent = None
    try:
        personal_all_courts_result_defeat_percent = all_personal_courts_defeat / only_win_or_defeat_all_courts * 100
    except ZeroDivisionError:
        personal_all_courts_result_defeat_percent = None
    try:
        personal_civil_courts_result_win_percent = civil_personal_courts_win / only_win_or_defeat_civil * 100
    except ZeroDivisionError:
        personal_civil_courts_result_win_percent = None
    try:
        personal_civil_courts_result_defeat_percent = civil_personal_courts_defeat / only_win_or_defeat_civil * 100
    except ZeroDivisionError:
        personal_civil_courts_result_defeat_percent = None
    try:
        personal_criminal_courts_result_win_percent = criminal_personal_courts_win / only_win_or_defeat_criminal * 100
    except ZeroDivisionError:
        personal_criminal_courts_result_win_percent = None
    try:
        personal_criminal_courts_result_defeat_percent = criminal_personal_courts_defeat / only_win_or_defeat_criminal * 100
    except ZeroDivisionError:
        personal_criminal_courts_result_defeat_percent = None
    try:
        personal_administrical_proceedings_courts_result_win_percent = administrical_proceedings_personal_courts_win / only_win_or_defeat_administrical_proceedings* 100
    except ZeroDivisionError:
        personal_administrical_proceedings_courts_result_win_percent = None
    try:
        personal_administrical_proceedings_courts_result_defeat_percent = administrical_proceedings_personal_courts_defeat / only_win_or_defeat_administrical_proceedings * 100
    except ZeroDivisionError:
        personal_administrical_proceedings_courts_result_defeat_percent = None
    try:
        personal_administrical_offence_courts_result_win_percent = administrical_offence_personal_courts_win / only_win_or_defeat_administrical_offence * 100
    except ZeroDivisionError:
        personal_administrical_offence_courts_result_win_percent = None
    try:
        personal_administrical_offence_courts_result_defeat_percent = administrical_offence_personal_courts_defeat / only_win_or_defeat_administrical_offence * 100
    except ZeroDivisionError:
        personal_administrical_offence_courts_result_defeat_percent = None

    month_year_filter = MonthYearAllStatisticsFilter(request.GET)
    if month_year_filter.is_valid():
        # проверка на использование формы
        use_form_check = True
        # Все выйгранные дела сотрудника с применением фильтра
        all_personal_courts_win = Courts.objects.filter(Q(is_complete=True) & Q(responsible=request.user) & Q(court_result=1) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()

        # Все выйгранные гражданские дела сотрудника
        civil_personal_courts_win = Courts.objects.filter(
            Q(is_complete=True) & Q(type_proceedings_choises=1) & Q(court_result=1) & Q(
                responsible=request.user) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # Все выйгранные уголовные дела сотрудника
        criminal_personal_courts_win = Courts.objects.filter(
            Q(is_complete=True) & Q(type_proceedings_choises=2) & Q(court_result=1) & Q(
                responsible=request.user) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # Все выйгранные дела (КАС) сотрудника
        administrical_proceedings_personal_courts_win = Courts.objects.filter(
            Q(is_complete=True) & Q(court_result=1) & Q(type_proceedings_choises=3) & Q(
                responsible=request.user) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # Все выйгранные дела (КоАП) сотрудника
        administrical_offence_personal_courts_win = Courts.objects.filter(
            Q(is_complete=True) & Q(court_result=1) & Q(type_proceedings_choises=4) & Q(
                responsible=request.user) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()

        # Все проигранные дела сотрудника
        all_personal_courts_defeat = Courts.objects.filter(
            Q(is_complete=True) & Q(responsible=request.user) & Q(court_result=2) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()

        # Все проигранные гражданские дела сотрудника
        civil_personal_courts_defeat = Courts.objects.filter(
            Q(is_complete=True) & Q(type_proceedings_choises=1) & Q(court_result=2) & Q(
                responsible=request.user) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # Все проигранные уголовные дела сотрудника
        criminal_personal_courts_defeat = Courts.objects.filter(
            Q(is_complete=True) & Q(type_proceedings_choises=2) & Q(court_result=2) & Q(
                responsible=request.user) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # Все проигранные дела (КАС) сотрудника
        administrical_proceedings_personal_courts_defeat = Courts.objects.filter(
            Q(is_complete=True) & Q(court_result=2) & Q(type_proceedings_choises=3) & Q(
                responsible=request.user) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()
        # Все проигранные дела (КоАП) сотрудника
        administrical_offence_personal_courts_defeat = Courts.objects.filter(
            Q(is_complete=True) & Q(court_result=2) & Q(type_proceedings_choises=4) & Q(
                responsible=request.user) & Q(date_of_judgment__range=(
        month_year_filter.cleaned_data["from_year_month"], month_year_filter.cleaned_data["to_year_month"]))).count()

        only_win_or_defeat_all_courts = all_personal_courts_win + all_personal_courts_defeat
        only_win_or_defeat_civil = civil_personal_courts_win + civil_personal_courts_defeat
        only_win_or_defeat_criminal = criminal_personal_courts_win + criminal_personal_courts_defeat
        only_win_or_defeat_administrical_proceedings = administrical_proceedings_personal_courts_win + administrical_proceedings_personal_courts_defeat
        only_win_or_defeat_administrical_offence = administrical_offence_personal_courts_win + administrical_offence_personal_courts_defeat

        try:
            personal_all_courts_result_win_percent = all_personal_courts_win / only_win_or_defeat_all_courts * 100
        except ZeroDivisionError:
            personal_all_courts_result_win_percent = None
        try:
            personal_all_courts_result_defeat_percent = all_personal_courts_defeat / only_win_or_defeat_all_courts * 100
        except ZeroDivisionError:
            personal_all_courts_result_defeat_percent = None
        try:
            personal_civil_courts_result_win_percent = civil_personal_courts_win / only_win_or_defeat_civil * 100
        except ZeroDivisionError:
            personal_civil_courts_result_win_percent = None
        try:
            personal_civil_courts_result_defeat_percent = civil_personal_courts_defeat / only_win_or_defeat_civil * 100
        except ZeroDivisionError:
            personal_civil_courts_result_defeat_percent = None
        try:
            personal_criminal_courts_result_win_percent = criminal_personal_courts_win / only_win_or_defeat_criminal * 100
        except ZeroDivisionError:
            personal_criminal_courts_result_win_percent = None
        try:
            personal_criminal_courts_result_defeat_percent = criminal_personal_courts_defeat / only_win_or_defeat_criminal * 100
        except ZeroDivisionError:
            personal_criminal_courts_result_defeat_percent = None
        try:
            personal_administrical_proceedings_courts_result_win_percent = administrical_proceedings_personal_courts_win / only_win_or_defeat_administrical_proceedings * 100
        except ZeroDivisionError:
            personal_administrical_proceedings_courts_result_win_percent = None
        try:
            personal_administrical_proceedings_courts_result_defeat_percent = administrical_proceedings_personal_courts_defeat / only_win_or_defeat_administrical_proceedings * 100
        except ZeroDivisionError:
            personal_administrical_proceedings_courts_result_defeat_percent = None
        try:
            personal_administrical_offence_courts_result_win_percent = administrical_offence_personal_courts_win / only_win_or_defeat_administrical_offence * 100
        except ZeroDivisionError:
            personal_administrical_offence_courts_result_win_percent = None
        try:
            personal_administrical_offence_courts_result_defeat_percent = administrical_offence_personal_courts_defeat / only_win_or_defeat_administrical_offence * 100
        except ZeroDivisionError:
            personal_administrical_offence_courts_result_defeat_percent = None


    return month_year_filter, all_personal_courts_win, civil_personal_courts_win, criminal_personal_courts_win, administrical_proceedings_personal_courts_win, \
           administrical_offence_personal_courts_win, all_personal_courts_defeat, civil_personal_courts_defeat, criminal_personal_courts_defeat, \
           administrical_proceedings_personal_courts_defeat, administrical_offence_personal_courts_defeat, \
           personal_all_courts_result_win_percent, personal_all_courts_result_defeat_percent, personal_civil_courts_result_win_percent, \
           personal_civil_courts_result_defeat_percent, personal_criminal_courts_result_win_percent, personal_criminal_courts_result_defeat_percent, \
           personal_administrical_proceedings_courts_result_win_percent, personal_administrical_proceedings_courts_result_defeat_percent, \
           personal_administrical_offence_courts_result_win_percent, personal_administrical_offence_courts_result_defeat_percent, use_form_check



# Статистика пользователей
# действующая нагрузка выбранного сотрудника
def users_statistic_load(request):
    # Объявляем все переменные, так как поля формы обязательные
    name = "Выберите"
    surname = "Сотрудника"
    choices_user_all_active_courts = None
    choices_user_all_active_courts_civil = None
    choices_user_all_active_courts_criminal = None
    choices_user_all_courts_administrical_offence = None
    choices_user_all_active_courts_administrical_proceedings = None

    choise_user_and_date_form = ChoiceUserAndDateFilter(request.POST)
    if choise_user_and_date_form.is_valid():
        try:
            name = choise_user_and_date_form.cleaned_data["responsible"].first_name
            surname = choise_user_and_date_form.cleaned_data["responsible"].last_name
        except AttributeError:
            name = "Выберите"
            surname = "Сотрудника"
        # Все активные суды выбранного сотрудника
        choices_user_all_active_courts = Courts.objects.filter(Q(is_complete=True) & Q(arhive=False) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"])).count()
        # гражданские активные судебные дела, за которые сотрудник ответственнен
        choices_user_all_active_courts_civil = Courts.objects.filter(
            Q(is_complete=True) & Q(arhive=False) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(type_proceedings_choises=1)).count()
        # уголовные активные судебные дела, за которые сотрудник ответственнен
        choices_user_all_active_courts_criminal = Courts.objects.filter(
            Q(is_complete=True) & Q(arhive=False) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(type_proceedings_choises=2)).count()
        # административные (КАС) активные судебные дела, за которые сотрудник ответственнен
        choices_user_all_active_courts_administrical_proceedings = Courts.objects.filter(
            Q(is_complete=True) & Q(arhive=False) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(type_proceedings_choises=3)).count()
        # административные (КоАП) активные судебные дела, за которые сотрудник ответственнен
        choices_user_all_courts_administrical_offence = Courts.objects.filter(
            Q(is_complete=True) & Q(arhive=False) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(type_proceedings_choises=4)).count()


    return choise_user_and_date_form, name, surname, choices_user_all_active_courts,choices_user_all_active_courts_civil, \
           choices_user_all_active_courts_criminal, choices_user_all_active_courts_administrical_proceedings, \
           choices_user_all_courts_administrical_offence

# Архив выбранного сотрудника (все дела)
def users_statistic_archive(request):
    # Объявляем все переменные, так как поля формы обязательные
    choices_user_all_courts_in_archive = None
    choices_user_all_courts_civil_in_archive = None
    choices_user_all_courts_civil_in_archive = None
    choices_user_all_courts_criminal_in_archive = None
    choices_user_all_courts_administrical_proceedings_in_archive = None
    choices_user_all_courts_administrical_offence_in_archive = None

    choise_user_and_date_form = ChoiceUserAndDateFilter(request.POST)
    if choise_user_and_date_form.is_valid():
        # Все активные суды выбранного сотрудника
        choices_user_all_courts_in_archive = Courts.objects.filter(Q(is_complete=True) & Q(arhive=True) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"])).count()
        # гражданские активные судебные дела, за которые сотрудник ответственнен
        choices_user_all_courts_civil_in_archive = Courts.objects.filter(
            Q(is_complete=True) & Q(arhive=True) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(type_proceedings_choises=1)).count()
        # уголовные активные судебные дела, за которые сотрудник ответственнен
        choices_user_all_courts_criminal_in_archive = Courts.objects.filter(
            Q(is_complete=True) & Q(arhive=True) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(type_proceedings_choises=2)).count()
        # административные (КАС) активные судебные дела, за которые сотрудник ответственнен
        choices_user_all_courts_administrical_proceedings_in_archive = Courts.objects.filter(
            Q(is_complete=True) & Q(arhive=True) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(type_proceedings_choises=3)).count()
        # административные (КоАП) активные судебные дела, за которые сотрудник ответственнен
        choices_user_all_courts_administrical_offence_in_archive = Courts.objects.filter(
            Q(is_complete=True) & Q(arhive=True) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(type_proceedings_choises=4)).count()


    return choices_user_all_courts_in_archive, choices_user_all_courts_civil_in_archive,choices_user_all_courts_criminal_in_archive, \
           choices_user_all_courts_administrical_proceedings_in_archive, choices_user_all_courts_administrical_offence_in_archive,


# статистика побед и поражений сотрудника
def choice_users_court_statistic_win_and_defeat(request):
    all_choice_users_courts_win = None
    civil_choice_users_courts_win = None
    criminal_choice_users_courts_win = None
    administrical_proceedings_choice_users_courts_win = None
    administrical_offence_choice_users_courts_win = None
    all_choice_users_courts_defeat = None
    civil_choice_users_courts_defeat = None
    criminal_choice_users_courts_defeat = None
    administrical_proceedings_choice_users_courts_defeat = None
    administrical_offence_choice_users_courts_defeat = None
    choice_users_all_courts_result_win_percent = None
    choice_users_all_courts_result_defeat_percent = None
    choice_users_civil_courts_result_win_percent = None
    choice_users_civil_courts_result_defeat_percent = None
    choice_users_criminal_courts_result_win_percent = None
    choice_users_criminal_courts_result_defeat_percent = None
    choice_users_administrical_proceedings_courts_result_win_percent = None
    choice_users_administrical_proceedings_courts_result_defeat_percent = None
    choice_users_administrical_offence_courts_result_win_percent = None
    choice_users_administrical_offence_courts_result_defeat_percent = None


    choise_user_and_date_form = ChoiceUserAndDateFilter(request.POST)
    if choise_user_and_date_form.is_valid():
        all_choice_users_courts_win = Courts.objects.filter(
            Q(is_complete=True) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(court_result=1) & Q(date_of_judgment__range=(
                choise_user_and_date_form.cleaned_data["from_year_month"],
                choise_user_and_date_form.cleaned_data["to_year_month"]))).count()

        # Все выйгранные гражданские дела сотрудника
        civil_choice_users_courts_win = Courts.objects.filter(
            Q(is_complete=True) & Q(type_proceedings_choises=1) & Q(court_result=1) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(date_of_judgment__range=(
                choise_user_and_date_form.cleaned_data["from_year_month"],
                choise_user_and_date_form.cleaned_data["to_year_month"]))).count()
        # Все выйгранные уголовные дела сотрудника
        criminal_choice_users_courts_win = Courts.objects.filter(
            Q(is_complete=True) & Q(type_proceedings_choises=2) & Q(court_result=1) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(date_of_judgment__range=(
                choise_user_and_date_form.cleaned_data["from_year_month"],
                choise_user_and_date_form.cleaned_data["to_year_month"]))).count()
        # Все выйгранные дела (КАС) сотрудника
        administrical_proceedings_choice_users_courts_win = Courts.objects.filter(
            Q(is_complete=True) & Q(court_result=1) & Q(type_proceedings_choises=3) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(date_of_judgment__range=(
                choise_user_and_date_form.cleaned_data["from_year_month"],
                choise_user_and_date_form.cleaned_data["to_year_month"]))).count()
        # Все выйгранные дела (КоАП) сотрудника
        administrical_offence_choice_users_courts_win = Courts.objects.filter(
            Q(is_complete=True) & Q(court_result=1) & Q(type_proceedings_choises=4) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(date_of_judgment__range=(
                choise_user_and_date_form.cleaned_data["from_year_month"],
                choise_user_and_date_form.cleaned_data["to_year_month"]))).count()

        # Все проигранные дела сотрудника
        all_choice_users_courts_defeat = Courts.objects.filter(
            Q(is_complete=True) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(court_result=2) & Q(date_of_judgment__range=(
                choise_user_and_date_form.cleaned_data["from_year_month"],
                choise_user_and_date_form.cleaned_data["to_year_month"]))).count()

        # Все проигранные гражданские дела сотрудника
        civil_choice_users_courts_defeat = Courts.objects.filter(
            Q(is_complete=True) & Q(type_proceedings_choises=1) & Q(court_result=2) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(date_of_judgment__range=(
                choise_user_and_date_form.cleaned_data["from_year_month"],
                choise_user_and_date_form.cleaned_data["to_year_month"]))).count()
        # Все проигранные уголовные дела сотрудника
        criminal_choice_users_courts_defeat = Courts.objects.filter(
            Q(is_complete=True) & Q(type_proceedings_choises=2) & Q(court_result=2) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(date_of_judgment__range=(
                choise_user_and_date_form.cleaned_data["from_year_month"],
                choise_user_and_date_form.cleaned_data["to_year_month"]))).count()
        # Все проигранные дела (КАС) сотрудника
        administrical_proceedings_choice_users_courts_defeat = Courts.objects.filter(
            Q(is_complete=True) & Q(court_result=2) & Q(type_proceedings_choises=3) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(date_of_judgment__range=(
                choise_user_and_date_form.cleaned_data["from_year_month"],
                choise_user_and_date_form.cleaned_data["to_year_month"]))).count()
        # Все проигранные дела (КоАП) сотрудника
        administrical_offence_choice_users_courts_defeat = Courts.objects.filter(
            Q(is_complete=True) & Q(court_result=2) & Q(type_proceedings_choises=4) & Q(responsible=choise_user_and_date_form.cleaned_data["responsible"]) & Q(date_of_judgment__range=(
                choise_user_and_date_form.cleaned_data["from_year_month"],
                choise_user_and_date_form.cleaned_data["to_year_month"]))).count()

        only_win_or_defeat_all_courts = all_choice_users_courts_win + all_choice_users_courts_defeat
        only_win_or_defeat_civil = civil_choice_users_courts_win + civil_choice_users_courts_defeat
        only_win_or_defeat_criminal = criminal_choice_users_courts_win + criminal_choice_users_courts_defeat
        only_win_or_defeat_administrical_proceedings = administrical_proceedings_choice_users_courts_win + administrical_proceedings_choice_users_courts_defeat
        only_win_or_defeat_administrical_offence = administrical_offence_choice_users_courts_win + administrical_offence_choice_users_courts_defeat

        try:
            choice_users_all_courts_result_win_percent = all_choice_users_courts_win / only_win_or_defeat_all_courts * 100
        except ZeroDivisionError:
            choice_users_all_courts_result_win_percent = None
        try:
            choice_users_all_courts_result_defeat_percent = all_choice_users_courts_defeat / only_win_or_defeat_all_courts * 100
        except ZeroDivisionError:
            choice_users_all_courts_result_defeat_percent = None
        try:
            choice_users_civil_courts_result_win_percent = civil_choice_users_courts_win / only_win_or_defeat_civil * 100
        except ZeroDivisionError:
            choice_users_civil_courts_result_win_percent = None
        try:
            choice_users_civil_courts_result_defeat_percent = civil_choice_users_courts_defeat / only_win_or_defeat_civil * 100
        except ZeroDivisionError:
            choice_users_civil_courts_result_defeat_percent = None
        try:
            choice_users_criminal_courts_result_win_percent = criminal_choice_users_courts_win / only_win_or_defeat_criminal * 100
        except ZeroDivisionError:
            choice_users_criminal_courts_result_win_percent = None
        try:
            choice_users_criminal_courts_result_defeat_percent = criminal_choice_users_courts_defeat / only_win_or_defeat_criminal * 100
        except ZeroDivisionError:
            choice_users_criminal_courts_result_defeat_percent = None
        try:
            choice_users_administrical_proceedings_courts_result_win_percent = administrical_proceedings_choice_users_courts_win / only_win_or_defeat_administrical_proceedings * 100
        except ZeroDivisionError:
            choice_users_administrical_proceedings_courts_result_win_percent = None
        try:
            choice_users_administrical_proceedings_courts_result_defeat_percent = administrical_proceedings_choice_users_courts_defeat / only_win_or_defeat_administrical_proceedings * 100
        except ZeroDivisionError:
            choice_users_administrical_proceedings_courts_result_defeat_percent = None
        try:
            choice_users_administrical_offence_courts_result_win_percent = administrical_offence_choice_users_courts_win / only_win_or_defeat_administrical_offence * 100
        except ZeroDivisionError:
            choice_users_administrical_offence_courts_result_win_percent = None
        try:
            choice_users_administrical_offence_courts_result_defeat_percent = administrical_offence_choice_users_courts_defeat / only_win_or_defeat_administrical_offence * 100
        except ZeroDivisionError:
            choice_users_administrical_offence_courts_result_defeat_percent = None

    return all_choice_users_courts_win, civil_choice_users_courts_win, criminal_choice_users_courts_win, administrical_proceedings_choice_users_courts_win, \
           administrical_offence_choice_users_courts_win, all_choice_users_courts_defeat, civil_choice_users_courts_defeat, criminal_choice_users_courts_defeat, \
           administrical_proceedings_choice_users_courts_defeat, administrical_offence_choice_users_courts_defeat, \
           choice_users_all_courts_result_win_percent, choice_users_all_courts_result_defeat_percent, choice_users_civil_courts_result_win_percent, \
           choice_users_civil_courts_result_defeat_percent, choice_users_criminal_courts_result_win_percent, choice_users_criminal_courts_result_defeat_percent, \
           choice_users_administrical_proceedings_courts_result_win_percent, choice_users_administrical_proceedings_courts_result_defeat_percent, \
           choice_users_administrical_offence_courts_result_win_percent, choice_users_administrical_offence_courts_result_defeat_percent