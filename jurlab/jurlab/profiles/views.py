from .models import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .forms import ProfileForm
from django.shortcuts import redirect
import datetime
from datetime import timedelta
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import online_users.models
from online_users.models import OnlineUserActivity
from django.contrib.auth.decorators import permission_required
from execution.models import Executions
from django.core.exceptions import ObjectDoesNotExist
from mainpage.models import Supervisor
from django.db.models import Q


@permission_required('profiles.view_profiles')
def profiles(request):
    if request.user.is_authenticated:
        profiles = Profiles.objects.all()
        user_activity = OnlineUserActivity.objects.all()
        user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=120))
        users = (user for user in user_status)
        # отображение количества непрочитаных судебных дел
        courts_read_count = Courts.objects.filter(Q(arhive=False) & Q(is_complete=True))
        # отображение количества непрочитаных испол производств
        execution_read_count = Executions.objects.filter(arhive=False)
        try:
            # объявляем переменную supervisor и пишем в нее данные
            supervisor = Supervisor.objects.get(court_author_vision=True)
            # если условие проходит, перезаписываем переменную courts_read_count
            if supervisor.court_author_vision == True:
                # courts_read_count - все суды, которые не в архиве и в которых пользователь создатель / ответственный / наблюдатель
                courts_read_count = Courts.objects.filter(
                    Q(author=request.user) | Q(responsible=request.user) | Q(observer=request.user) & (Q(arhive=False) & Q(is_complete=True)))
        # Окончание обработки ошибки. Если переменая supervisor == False, пишется переменная courts_read_count по умолчанию
        except ObjectDoesNotExist:
            courts_read_count = Courts.objects.filter(Q(arhive=False) & Q(is_complete=True))
        if request.user.is_staff | request.user.is_superuser:
            # Если пользователь админ или стаф, перезаписываем переменную снова
            courts_read_count = Courts.objects.filter(Q(arhive=False) & Q(is_complete=True))
        # Выводим, исходя из вычислений выше
        unread_courts_count = 0
        for court_obj in courts_read_count:
            for user_court_item in court_obj.read_court_users.all():
                if user_court_item == request.user:
                    unread_courts_count = unread_courts_count + 1
        try:
            # объявляем переменную supervisor и пишем в нее данные
            supervisor = Supervisor.objects.get(ex_author_vision=True)
            # если условие проходит, перезаписываем переменную courts
            if supervisor.ex_author_vision == True:
                # executions - все суды, которые не в архиве и в которых пользователь создатель / ответственный / наблюдатель
                execution_read_count = Executions.objects.filter(
                    Q(author=request.user) | Q(responsible=request.user) | Q(observer=request.user) & Q(arhive=False))
        # Окончание обработки ошибки. Если переменая supervisor == False, пишется по умолчанию
        except ObjectDoesNotExist:
            execution_read_count = Executions.objects.filter(arhive=False)
        # если пользователь руководитель или админ, отменяем все что сделали, если supervisor == True и показываем все
        if request.user.is_staff | request.user.is_superuser:
            execution_read_count = Executions.objects.filter(arhive=False)
        unread_executions_count = 0
        # перебираем объекты в переменной executions, если в списке не прочитанных испол производств есть пользователь то счетчик unread_executions_count +=1
        for ex_obj in execution_read_count:
            for user_ex_item in ex_obj.read_execution_users.all():
                if user_ex_item == request.user:
                    unread_executions_count = unread_executions_count + 1

        template = 'profiles/profiles_list.html'
        context = {
            'profiles':profiles,
            'user_status':user_status,
            'users':users,
            'user_activity':user_activity,
            'unread_executions_count':unread_executions_count,
            'unread_courts_count':unread_courts_count,




        }
        return render(request, template, context)
    return redirect('login_page')


@permission_required('profiles.view_profiles')
def myprofile(request):
    if request.user.is_authenticated:
        # отображение количества непрочитаных судебных дел
        courts_read_count = Courts.objects.filter(Q(arhive=False) & Q(is_complete=True))
        # отображение количества непрочитаных испол производств
        execution_read_count = Executions.objects.filter(arhive=False)
        try:
            # объявляем переменную supervisor и пишем в нее данные
            supervisor = Supervisor.objects.get(court_author_vision=True)
            # если условие проходит, перезаписываем переменную courts_read_count
            if supervisor.court_author_vision == True:
                # courts_read_count - все суды, которые не в архиве и в которых пользователь создатель / ответственный / наблюдатель
                courts_read_count = Courts.objects.filter(
                    Q(author=request.user) | Q(responsible=request.user) | Q(observer=request.user) & (Q(arhive=False) & Q(is_complete=True)))
        # Окончание обработки ошибки. Если переменая supervisor == False, пишется переменная courts_read_count по умолчанию
        except ObjectDoesNotExist:
            courts_read_count = Courts.objects.filter(Q(arhive=False) & Q(is_complete=True))
        if request.user.is_staff | request.user.is_superuser:
            # Если пользователь админ или стаф, перезаписываем переменную снова
            courts_read_count = Courts.objects.filter(Q(arhive=False) & Q(is_complete=True))
        # Выводим, исходя из вычислений выше
        unread_courts_count = 0
        for court_obj in courts_read_count:
            for user_court_item in court_obj.read_court_users.all():
                if user_court_item == request.user:
                    unread_courts_count = unread_courts_count + 1
        try:
            # объявляем переменную supervisor и пишем в нее данные
            supervisor = Supervisor.objects.get(ex_author_vision=True)
            # если условие проходит, перезаписываем переменную courts
            if supervisor.ex_author_vision == True:
                # executions - все суды, которые не в архиве и в которых пользователь создатель / ответственный / наблюдатель
                execution_read_count = Executions.objects.filter(
                    Q(author=request.user) | Q(responsible=request.user) | Q(observer=request.user) & Q(
                        arhive=False))
        # Окончание обработки ошибки. Если переменая supervisor == False, пишется по умолчанию
        except ObjectDoesNotExist:
            execution_read_count = Executions.objects.filter(arhive=False)
        # если пользователь руководитель или админ, отменяем все что сделали, если supervisor == True и показываем все
        if request.user.is_staff | request.user.is_superuser:
            execution_read_count = Executions.objects.filter(arhive=False)
        unread_executions_count = 0
        # перебираем объекты в переменной executions, если в списке не прочитанных испол производств есть пользователь то счетчик unread_executions_count +=1
        for ex_obj in execution_read_count:
            for user_ex_item in ex_obj.read_execution_users.all():
                if user_ex_item == request.user:
                    unread_executions_count = unread_executions_count + 1
        myprofile = Profiles.objects.all()
        template = 'profiles/myprofile.html'
        context = {
            'myprofile':myprofile,
            'unread_executions_count': unread_executions_count,
            'unread_courts_count': unread_courts_count,
        }
        return render(request, template, context)
    return redirect('login_page')
    
@permission_required('profiles.view_profiles')
def profile_detail(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profiles, pk=pk)
        user_activity = OnlineUserActivity.objects.get(user_id=profile.user.id)
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form = form.save(commit=False)
                profile.save()
                return redirect(profile_detail, pk)
        else:
            form = ProfileForm(instance=profile)
        # отображение количества непрочитаных судебных дел
        courts_read_count = Courts.objects.filter(Q(arhive=False) & Q(is_complete=True))
        # отображение количества непрочитаных испол производств
        execution_read_count = Executions.objects.filter(arhive=False)
        try:
            # объявляем переменную supervisor и пишем в нее данные
            supervisor = Supervisor.objects.get(court_author_vision=True)
            # если условие проходит, перезаписываем переменную courts_read_count
            if supervisor.court_author_vision == True:
                # courts_read_count - все суды, которые не в архиве и в которых пользователь создатель / ответственный / наблюдатель
                courts_read_count = Courts.objects.filter(
                    Q(author=request.user) | Q(responsible=request.user) | Q(observer=request.user) & (Q(arhive=False) & Q(is_complete=True)))
        # Окончание обработки ошибки. Если переменая supervisor == False, пишется переменная courts_read_count по умолчанию
        except ObjectDoesNotExist:
            courts_read_count = Courts.objects.filter(Q(arhive=False) & Q(is_complete=True))
        if request.user.is_staff | request.user.is_superuser:
            # Если пользователь админ или стаф, перезаписываем переменную снова
            courts_read_count = Courts.objects.filter(Q(arhive=False) & Q(is_complete=True))
        # Выводим, исходя из вычислений выше
        unread_courts_count = 0
        for court_obj in courts_read_count:
            for user_court_item in court_obj.read_court_users.all():
                if user_court_item == request.user:
                    unread_courts_count = unread_courts_count + 1
        try:
            # объявляем переменную supervisor и пишем в нее данные
            supervisor = Supervisor.objects.get(ex_author_vision=True)
            # если условие проходит, перезаписываем переменную courts
            if supervisor.ex_author_vision == True:
                # executions - все суды, которые не в архиве и в которых пользователь создатель / ответственный / наблюдатель
                execution_read_count = Executions.objects.filter(
                    Q(author=request.user) | Q(responsible=request.user) | Q(observer=request.user) & Q(
                        arhive=False))
        # Окончание обработки ошибки. Если переменая supervisor == False, пишется по умолчанию
        except ObjectDoesNotExist:
            execution_read_count = Executions.objects.filter(arhive=False)
        # если пользователь руководитель или админ, отменяем все что сделали, если supervisor == True и показываем все
        if request.user.is_staff | request.user.is_superuser:
            execution_read_count = Executions.objects.filter(arhive=False)
        unread_executions_count = 0
        # перебираем объекты в переменной executions, если в списке не прочитанных испол производств есть пользователь то счетчик unread_executions_count +=1
        for ex_obj in execution_read_count:
            for user_ex_item in ex_obj.read_execution_users.all():
                if user_ex_item == request.user:
                    unread_executions_count = unread_executions_count + 1
        template = 'profiles/profile_detail.html'
        context = {
            'profile': profile,
            'form': form,
            'user_activity':user_activity,
            'unread_executions_count': unread_executions_count,
            'unread_courts_count': unread_courts_count,



        }
        return render(request, template, context)
    return redirect('login_page')


