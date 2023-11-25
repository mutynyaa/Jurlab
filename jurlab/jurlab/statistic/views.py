from django.shortcuts import render
from courts.models import Courts
from execution.models import Executions
from django.db.models import Sum
from django.contrib.auth.decorators import permission_required
from execution.models import Executions
from django.core.exceptions import ObjectDoesNotExist
from mainpage.models import Supervisor
from django.db.models import Q
from . import services_statistic
from .forms import MonthYearAllStatisticsFilter, ChoiceUserAndDateFilter

def all_statistic(request):
    # Все судебные дела
    all_courts, all_courts_win, all_courts_defeat,\
    all_courts_result_win_percent, all_courts_result_defeat_percent, month_year_filter, all_active_courts,\
    all_courts_in_archive = services_statistic.all_court_statistics_logic(request)
    # Гражданские дела
    all_civil_courts, all_civil_courts_win, all_civil_courts_defeat, \
    all_civil_courts_result_win_percent, all_civil_courts_result_defeat_percent, all_active_civil_courts, \
    all_civil_courts_in_archive = services_statistic.civil_court_statistics_logic(request)
    # Уголовные дела
    all_criminal_courts, all_criminal_courts_win, all_criminal_courts_defeat, \
    all_criminal_courts_result_win_percent, all_criminal_courts_result_defeat_percent, all_active_criminal_courts, \
    all_criminal_courts_in_archive = services_statistic.criminal_court_statistics_logic(request)
    # Административные дела (КАС)
    all_administrical_proceedings_courts, all_administrical_proceedings_courts_win, all_administrical_proceedings_courts_defeat, \
    all_administrical_proceedings_courts_result_win_percent, all_administrical_proceedings_courts_result_defeat_percent,all_active_administrical_proceedings_courts, \
    all_administrical_proceedings_courts_in_archive = services_statistic.administrical_proceedings_court_statistics_logic(request)
    # Административные дела (КоАП)
    all_administrical_offence_courts, all_administrical_offence_courts_win, all_administrical_offence_courts_defeat, \
    all_administrical_offence_courts_result_win_percent, all_administrical_offence_courts_result_defeat_percent, all_active_administrical_offence_courts, \
    all_administrical_offence_courts_in_archive = services_statistic.administrical_offence_court_statistics_logic(request)

    context = {
            # Форма фильтра по датам
            'month_year_filter': month_year_filter,
            # Все судебные дела
            'all_courts':all_courts,
            'all_courts_win':all_courts_win,
            'all_courts_defeat':all_courts_defeat,
            'all_courts_result_win_percent':all_courts_result_win_percent,
            'all_courts_result_defeat_percent':all_courts_result_defeat_percent,
            'all_active_courts': all_active_courts,
            'all_courts_in_archive': all_courts_in_archive,
            # Гражданские дела
            'all_civil_courts':all_civil_courts,
            'all_civil_courts_win':all_civil_courts_win,
            'all_civil_courts_defeat':all_civil_courts_defeat,
            'all_civil_courts_result_win_percent':all_civil_courts_result_win_percent,
            'all_civil_courts_result_defeat_percent':all_civil_courts_result_defeat_percent,
            'all_active_civil_courts':all_active_civil_courts,
            'all_civil_courts_in_archive':all_civil_courts_in_archive,
            # Уголовные дела
            'all_criminal_courts':all_criminal_courts,
            'all_criminal_courts_win':all_criminal_courts_win,
            'all_criminal_courts_defeat':all_criminal_courts_defeat,
            'all_criminal_courts_result_win_percent':all_criminal_courts_result_win_percent,
            'all_criminal_courts_result_defeat_percent':all_criminal_courts_result_defeat_percent,
            'all_active_criminal_courts':all_active_criminal_courts,
            'all_criminal_courts_in_archive':all_criminal_courts_in_archive,
            # Административные дела (КАС)
            'all_administrical_proceedings_courts': all_administrical_proceedings_courts,
            'all_administrical_proceedings_courts_win': all_administrical_proceedings_courts_win,
            'all_administrical_proceedings_courts_defeat': all_administrical_proceedings_courts_defeat,
            'all_administrical_proceedings_courts_result_win_percent': all_administrical_proceedings_courts_result_win_percent,
            'all_administrical_proceedings_courts_result_defeat_percent': all_administrical_proceedings_courts_result_defeat_percent,
            'all_active_administrical_proceedings_courts': all_active_administrical_proceedings_courts,
            'all_administrical_proceedings_courts_in_archive': all_administrical_proceedings_courts_in_archive,
            # Административные дела (КоАП)
            'all_administrical_offence_courts': all_administrical_offence_courts,
            'all_administrical_offence_courts_win': all_administrical_offence_courts_win,
            'all_administrical_offence_courts_defeat': all_administrical_offence_courts_defeat,
            'all_administrical_offence_courts_result_win_percent': all_administrical_offence_courts_result_win_percent,
            'all_administrical_offence_courts_result_defeat_percent': all_administrical_offence_courts_result_defeat_percent,
            'all_active_administrical_offence_courts': all_active_administrical_offence_courts,
            'all_administrical_offence_courts_in_archive': all_administrical_offence_courts_in_archive,



    }
    template = 'statistic/all_statistic.html'
    return render(request, template, context)

# Логика статистики "Личная статистика"
def personal_statistic(request):
    # действующая нагрузка сотрудника
    all_active_personal_courts, all_active_personal_courts_civil, all_active_personal_courts_criminal, all_active_personal_courts_administrical_proceedings, \
    all_active_personal_courts_administrical_offence = services_statistic.personal_court_statistic_load(request)

    # Архив сотрудника (все дела)
    all_personal_courts_in_archive, all_personal_courts_civil_in_archive, all_personal_courts_criminal_in_archive, all_personal_courts_administrical_proceedings_in_archive, \
    all_personal_courts_administrical_offence_in_archive = services_statistic.personal_court_statistic_archive(request)

    # Статистика побед и поражений сотрудника
    month_year_filter, all_personal_courts_win, civil_personal_courts_win, criminal_personal_courts_win, administrical_proceedings_personal_courts_win, \
    administrical_offence_personal_courts_win, all_personal_courts_defeat, civil_personal_courts_defeat, criminal_personal_courts_defeat, \
    administrical_proceedings_personal_courts_defeat, administrical_offence_personal_courts_defeat, \
    personal_all_courts_result_win_percent, personal_all_courts_result_defeat_percent, personal_civil_courts_result_win_percent, \
    personal_civil_courts_result_defeat_percent, personal_criminal_courts_result_win_percent, personal_criminal_courts_result_defeat_percent, \
    personal_administrical_proceedings_courts_result_win_percent, personal_administrical_proceedings_courts_result_defeat_percent, \
    personal_administrical_offence_courts_result_win_percent, personal_administrical_offence_courts_result_defeat_percent, use_form_check= services_statistic.personal_court_statistic_win_and_defeat(request)

    context = {
        # проверка на использование формы
        'use_form_check':use_form_check,
        # фильтр даты
        'month_year_filter':month_year_filter,
        # действующая нагрузка сотрудника
        'all_active_personal_courts':all_active_personal_courts,
        'all_active_personal_courts_civil': all_active_personal_courts_civil,
        'all_active_personal_courts_criminal': all_active_personal_courts_criminal,
        'all_active_personal_courts_administrical_proceedings': all_active_personal_courts_administrical_proceedings,
        'all_active_personal_courts_administrical_offence': all_active_personal_courts_administrical_offence,

        # Архив сотрудника (все дела)
        'all_personal_courts_in_archive': all_personal_courts_in_archive,
        'all_personal_courts_civil_in_archive': all_personal_courts_civil_in_archive,
        'all_personal_courts_criminal_in_archive': all_personal_courts_criminal_in_archive,
        'all_personal_courts_administrical_proceedings_in_archive': all_personal_courts_administrical_proceedings_in_archive,
        'all_personal_courts_administrical_offence_in_archive': all_personal_courts_administrical_offence_in_archive,

        # Статистика побед и поражений сотрудника
        'all_personal_courts_win':all_personal_courts_win,
        'civil_personal_courts_win': civil_personal_courts_win,
        'criminal_personal_courts_win': criminal_personal_courts_win,
        'administrical_proceedings_personal_courts_win': administrical_proceedings_personal_courts_win,
        'administrical_offence_personal_courts_win': administrical_offence_personal_courts_win,
        'all_personal_courts_defeat': all_personal_courts_defeat,
        'civil_personal_courts_defeat': civil_personal_courts_defeat,
        'criminal_personal_courts_defeat':criminal_personal_courts_defeat,
        'administrical_proceedings_personal_courts_defeat': administrical_proceedings_personal_courts_defeat,
        'administrical_offence_personal_courts_defeat': administrical_offence_personal_courts_defeat,
        'personal_all_courts_result_win_percent': personal_all_courts_result_win_percent,
        'personal_all_courts_result_defeat_percent': personal_all_courts_result_defeat_percent,
        'personal_civil_courts_result_win_percent': personal_civil_courts_result_win_percent,
        'personal_civil_courts_result_defeat_percent': personal_civil_courts_result_defeat_percent,
        'personal_criminal_courts_result_win_percent': personal_criminal_courts_result_win_percent,
        'personal_criminal_courts_result_defeat_percent': personal_criminal_courts_result_defeat_percent,
        'personal_administrical_proceedings_courts_result_win_percent': personal_administrical_proceedings_courts_result_win_percent,
        'personal_administrical_proceedings_courts_result_defeat_percent': personal_administrical_proceedings_courts_result_defeat_percent,
        'personal_administrical_offence_courts_result_win_percent': personal_administrical_offence_courts_result_win_percent,
        'personal_administrical_offence_courts_result_defeat_percent':personal_administrical_offence_courts_result_defeat_percent,








    }
    template = 'statistic/personal_statistic.html'
    return render(request, template, context)


# Логика статистики "Статистика выбранного пользователя"
def users_statistic(request):
    # статистика активных судебных дел выбранного пользователя
    choise_user_and_date_form, name, surname, choices_user_all_active_courts, choices_user_all_active_courts_civil, \
    choices_user_all_active_courts_criminal, choices_user_all_active_courts_administrical_proceedings, \
    choices_user_all_courts_administrical_offence = services_statistic.users_statistic_load(request)
    # статистика судебных дел в архиве выбранного пользователя
    choices_user_all_courts_in_archive, choices_user_all_courts_civil_in_archive, choices_user_all_courts_criminal_in_archive, \
    choices_user_all_courts_administrical_proceedings_in_archive, choices_user_all_courts_administrical_offence_in_archive = services_statistic.users_statistic_archive(request)

    # Статистика побед и поражений выбранного сотрудника
    all_choice_users_courts_win, civil_choice_users_courts_win, criminal_choice_users_courts_win, administrical_proceedings_choice_users_courts_win, \
    administrical_offence_choice_users_courts_win, all_choice_users_courts_defeat, civil_choice_users_courts_defeat, criminal_choice_users_courts_defeat, \
    administrical_proceedings_choice_users_courts_defeat, administrical_offence_choice_users_courts_defeat, \
    choice_users_all_courts_result_win_percent, choice_users_all_courts_result_defeat_percent, choice_users_civil_courts_result_win_percent, \
    choice_users_civil_courts_result_defeat_percent, choice_users_criminal_courts_result_win_percent, choice_users_criminal_courts_result_defeat_percent, \
    choice_users_administrical_proceedings_courts_result_win_percent, choice_users_administrical_proceedings_courts_result_defeat_percent, \
    choice_users_administrical_offence_courts_result_win_percent, choice_users_administrical_offence_courts_result_defeat_percent = services_statistic.choice_users_court_statistic_win_and_defeat(request)

    use_form_check = choise_user_and_date_form.cleaned_data["responsible"]
    context = {
        # Общие переменные
        'choise_user_and_date_form':choise_user_and_date_form,
        'name':name,
        'surname':surname,

        # статистика активных судебных дел выбранного пользователя
        'choices_user_all_active_courts':choices_user_all_active_courts,
        'choices_user_all_active_courts_civil':choices_user_all_active_courts_civil,
        'choices_user_all_active_courts_criminal':choices_user_all_active_courts_criminal,
        'choices_user_all_active_courts_administrical_proceedings':choices_user_all_active_courts_administrical_proceedings,
        'choices_user_all_courts_administrical_offence':choices_user_all_courts_administrical_offence,

        # статистика судебных дел в архиве выбранного пользователя
        'choices_user_all_courts_in_archive': choices_user_all_courts_in_archive,
        'choices_user_all_courts_civil_in_archive': choices_user_all_courts_civil_in_archive,
        'choices_user_all_courts_criminal_in_archive': choices_user_all_courts_criminal_in_archive,
        'choices_user_all_courts_administrical_proceedings_in_archive': choices_user_all_courts_administrical_proceedings_in_archive,
        'choices_user_all_courts_administrical_offence_in_archive': choices_user_all_courts_administrical_offence_in_archive,

        # Статистика побед и поражений выбранного сотрудника
        'all_choice_users_courts_win': all_choice_users_courts_win,
        'civil_choice_users_courts_win': civil_choice_users_courts_win,
        'criminal_choice_users_courts_win': criminal_choice_users_courts_win,
        'administrical_proceedings_choice_users_courts_win': administrical_proceedings_choice_users_courts_win,
        'administrical_offence_choice_users_courts_win': administrical_offence_choice_users_courts_win,
        'all_choice_users_courts_defeat': all_choice_users_courts_defeat,
        'civil_choice_users_courts_defeat': civil_choice_users_courts_defeat,
        'criminal_choice_users_courts_defeat': criminal_choice_users_courts_defeat,
        'administrical_proceedings_choice_users_courts_defeat': administrical_proceedings_choice_users_courts_defeat,
        'administrical_offence_choice_users_courts_defeat': administrical_offence_choice_users_courts_defeat,
        'choice_users_all_courts_result_win_percent': choice_users_all_courts_result_win_percent,
        'choice_users_all_courts_result_defeat_percent': choice_users_all_courts_result_defeat_percent,
        'choice_users_civil_courts_result_win_percent': choice_users_civil_courts_result_win_percent,
        'choice_users_civil_courts_result_defeat_percent': choice_users_civil_courts_result_defeat_percent,
        'choice_users_criminal_courts_result_win_percent': choice_users_criminal_courts_result_win_percent,
        'choice_users_criminal_courts_result_defeat_percent': choice_users_criminal_courts_result_defeat_percent,
        'choice_users_administrical_proceedings_courts_result_win_percent': choice_users_administrical_proceedings_courts_result_win_percent,
        'choice_users_administrical_proceedings_courts_result_defeat_percent': choice_users_administrical_proceedings_courts_result_defeat_percent,
        'choice_users_administrical_offence_courts_result_win_percent': choice_users_administrical_offence_courts_result_win_percent,
        'choice_users_administrical_offence_courts_result_defeat_percent': choice_users_administrical_offence_courts_result_defeat_percent,





        # проверяем, выбран ли пользователь в форме
        'use_form_check':use_form_check,


    }
    template = 'statistic/users_statistic.html'
    return render(request, template, context)
