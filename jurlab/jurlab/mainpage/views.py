from django.shortcuts import render
from .models import Post, Supervisor
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import AuthUserForm, RegisterUserForm, SupervisorForm
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate
from django import template
from profiles.models import Profiles
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required
from courts.models import Courts
from execution.models import Executions
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

#return redirect('courts_detail', pk=courts.pk)




def mainpage(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
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
                courts_read_count = Courts.objects.filter(Q(author=request.user) | Q(responsible=request.user) | Q(observer=request.user) & (Q(arhive=False) & Q(is_complete=True)))
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
                execution_read_count = Executions.objects.filter(Q(author=request.user) | Q(responsible=request.user) | Q(observer=request.user) & Q(arhive=False))
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
        template = 'mainpage/mainpage_list.html'
        context = {
            'posts':posts,
            'unread_courts_count':unread_courts_count,
            'unread_executions_count':unread_executions_count,
        }
        return render(request, template, context)
    else:
        return redirect('login_page')


@permission_required('mainpage.view_supervisor')    
def supervisor(request):
    if request.user.is_authenticated:
        uncomplete_courts_count = Courts.objects.filter(is_complete=False).count()
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
        law = Supervisor.objects.all()
        supervisor_court_author_vision = Supervisor.objects.get(title__startswith="Сотрудники видят только свои суды")
        if request.method == "POST":
            form = SupervisorForm(request.POST, instance=supervisor_court_author_vision)
            if form.is_valid():
                form.save(commit=False)
                supervisor_court_author_vision.save()
                return redirect('supervisor')
        else:
            form = SupervisorForm(instance=supervisor_court_author_vision)
        template = 'mainpage/supervisor_list.html'
        context = {
            'law':law,
            'form':form,
            'supervisor_court_author_vision':supervisor_court_author_vision,
            'unread_courts_count':unread_courts_count,
            'unread_executions_count':unread_executions_count,
            'uncomplete_courts_count':uncomplete_courts_count,

        }
        return render(request, template, context)
    else:
        return redirect('login_page')

def clear_uncomplete_courts(request):
    if request.user.is_staff:
        uncomplete_courts = Courts.objects.filter(is_complete=False)
        for item in uncomplete_courts:
            item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('login_page')

class JurlabLoginView(LoginView):
    template_name = 'mainpage/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('mainpage')
    def get_success_url(self):
        return self.success_url


class JurlabLogout(LogoutView):
    next_page = reverse_lazy('login_page')
    


register = template.Library() 
@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
    
    
def profile_detail(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profiles, pk=pk)
        template = 'profiles/profile_detail.html'
        context = {
            'profile': profile
        }
        return render(request, template, context)
    else:
        return redirect('login_page')