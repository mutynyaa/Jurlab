from django.core.exceptions import ObjectDoesNotExist
from .models import Executions
from django.db.models import Q
from django.contrib.auth.models import User, Group
from courts.models import Courts
from mainpage.models import Supervisor



def unread_executions_counter_and_var_execution_read_count_logic(request):
    execution_read_count = Executions.objects.filter(arhive=False)
    try:
        # объявляем переменную supervisor и пишем в нее данные
        supervisor = Supervisor.objects.get(ex_author_vision=True)
        # если условие проходит, перезаписываем переменную execution_read_count
        if supervisor.ex_author_vision == True:
            # executions - все суды, которые не в архиве и в которых пользователь создатель / ответственный / наблюдатель
            execution_read_count = Executions.objects.filter(
                Q(author=request.user) | Q(responsible=request.user) | Q(observer=request.user) & Q(arhive=False)).distinct()
        # Окончание обработки ошибки. Если переменая supervisor == False, пишется по умолчанию
    except ObjectDoesNotExist:
        execution_read_count = Executions.objects.filter(Q(arhive=False))
        # если пользователь руководитель или админ, отменяем все что сделали, если supervisor == True и показываем все
    if request.user.is_staff | request.user.is_superuser:
        execution_read_count = Executions.objects.filter(Q(arhive=False))
    unread_executions_count = 0
    for ex_obj in execution_read_count:
        for user_ex_item in ex_obj.read_execution_users.all():
            if user_ex_item == request.user:
                unread_executions_count = unread_executions_count + 1

    return unread_executions_count, execution_read_count


