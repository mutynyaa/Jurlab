from django.core.exceptions import ObjectDoesNotExist
from execution.models import Executions
from django.db.models import Q
from django.contrib.auth.models import User, Group
from .models import Courts
from mainpage.models import Supervisor
from django.shortcuts import get_object_or_404

def unread_court_counter_and_var_courts_logic(request):
    courts = Courts.objects.filter(Q(arhive=False) & Q(is_complete=True))
    # обработка ошибки, если режим "вижу только мои суды" выключен. Пробуем.
    try:
        # объявляем переменную supervisor и пишем в нее данные
        supervisor = Supervisor.objects.get(court_author_vision=True)
        # если условие проходит, перезаписываем переменную courts
        if supervisor.court_author_vision == True:
            # courts - все суды, которые не в архиве и в которых пользователь создатель / ответственный / наблюдатель
            courts = Courts.objects.filter(
                Q(author=request.user) | Q(responsible=request.user) | Q(observer=request.user) & Q(arhive=False) & Q(
                    is_complete=True)).distinct()
    # Окончание обработки ошибки. Если переменая supervisor == False, пишется по умолчанию
    except ObjectDoesNotExist:
        courts = Courts.objects.filter(Q(arhive=False) & Q(is_complete=True))
    # если пользователь руководитель или админ, отменяем все что сделали, если supervisor == True и показываем все
    if request.user.is_staff | request.user.is_superuser:
        courts = Courts.objects.filter(Q(arhive=False) & Q(is_complete=True))
    # отображение количества непрочитанных судов
    unread_courts_count = 0
    # перебираем объекты в переменной courts, если в списке не прочитанных судов есть пользователь то счетчик unread_courts_count +=1
    for court_obj in courts:
        for user_court_item in court_obj.read_court_users.all():
            if user_court_item == request.user:
                unread_courts_count = unread_courts_count + 1
    return unread_courts_count, courts




