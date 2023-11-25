from django.shortcuts import render
from .models import Courts, CommentsCourts, CourtDocuments, CourtJudgment
from django.utils import timezone
from django.contrib.auth.models import User, Group
from .forms import CourtsFormRedact, CommentForm, CourtsFormNew, DocumentForm, FilterForm, CategoryFilterForm, CourtSearchForm, JudgmentForm, DeleteCommentForm, CourtsFormNewStepTwo
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from profiles.models import Profiles
from django.core.paginator import Paginator, InvalidPage
from mainpage.models import Supervisor
from django.db.models import Q
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.core.files.base import ContentFile
import datetime
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from execution.models import Executions
from . import services_courts
from execution import services_executions



# view для страницы формы создания нового судебного дела (шаг 1)
@login_required
@permission_required(['courts.view_courts', 'courts.add_courts'])
def courts_new(request):
    # присваиваем значения unread_executions_count и execution_read_count из функции unread_executions_counter_and_var_execution_read_count_logic
    unread_executions_count, execution_read_count = services_executions.unread_executions_counter_and_var_execution_read_count_logic(
        request)
    # присваиваем значения unread_courts_count и courts из функции unread_court_counter_and_var_courts_logic
    unread_courts_count, courts = services_courts.unread_court_counter_and_var_courts_logic(request)
    # Удаление незаконченных объектов модели courts
    all_courts = Courts.objects.all()
    today = datetime.datetime.now().date()
    for court_item in all_courts:
        uncomplete_court_date = court_item.created_date + timedelta(days=1)
        if today >= uncomplete_court_date and court_item.is_complete == False:
            court_item.delete()
    # Создаем новый суд с помощью формы // create now court with help form
    all_users = User.objects.all()
    if request.method == "POST":
        form = CourtsFormNew(request.POST)
        if form.is_valid():
            court_new = form.save(commit=False)
            # Автор - пользователь, который создал суд // author - is user which create this court
            court_new.author = request.user
            # Ответственный - пользователь, который создал суд
            court_new.responsible = request.user
            # Дата создания суда
            court_new.created_date = datetime.datetime.now()
            court_new.save()
            form.save_m2m()
            # Устанавливаем всех пользователей в поле courts.read_court_users в True
            for user_item in all_users:
                court_new.read_court_users.add(user_item)
            return redirect('court_new_step_two', pk=court_new.pk)
    else:
        form = CourtsFormNew()
    return render(request, 'courts/courts_new.html',{'form':form, 'unread_courts_count':unread_courts_count,'unread_executions_count':unread_executions_count,})


# view для страницы формы создания нового судебного дела (шаг 2)
@login_required
@permission_required(['courts.view_courts', 'courts.add_courts'])
def court_new_step_two(request, pk):
    # присваиваем значения unread_executions_count и execution_read_count из функции unread_executions_counter_and_var_execution_read_count_logic
    unread_executions_count, execution_read_count = services_executions.unread_executions_counter_and_var_execution_read_count_logic(
        request)
    # присваиваем значения unread_courts_count и courts из функции unread_court_counter_and_var_courts_logic
    unread_courts_count, courts = services_courts.unread_court_counter_and_var_courts_logic(request)
    court_new_step_two = get_object_or_404(Courts, pk=pk)
    if request.method == "POST":
        form_new_step_two = CourtsFormNewStepTwo(request.POST, instance=court_new_step_two)
        if form_new_step_two.is_valid():
            court_new_step_two = form_new_step_two.save(commit=False)
            court_new_step_two.last_change_make_user = request.user
            court_new_step_two.is_complete = True
            court_new_step_two.save()
            form_new_step_two.save_m2m()
            return redirect('courts_detail', pk=court_new_step_two.pk)
    else:
        form_new_step_two = CourtsFormNewStepTwo(instance=court_new_step_two)
        template = 'courts/courts_new_step_two.html'
        context = {
            'court_new_step_two': court_new_step_two,
            'form_new_step_two': form_new_step_two,
            'unread_executions_count': unread_executions_count,
            'unread_courts_count': unread_courts_count,

        }
        return render(request, template, context)


# view для основной страницы судебного дела
@login_required
@permission_required('courts.view_courts')
def court(request):
    # присваиваем значения unread_executions_count и execution_read_count из функции unread_executions_counter_and_var_execution_read_count_logic
        unread_executions_count, execution_read_count = services_executions.unread_executions_counter_and_var_execution_read_count_logic(request)
    # присваиваем значения unread_courts_count и courts из функции unread_court_counter_and_var_courts_logic
        unread_courts_count, courts = services_courts.unread_court_counter_and_var_courts_logic(request)
    # Поиск судебных дел / search court list
        search_court = request.GET.get('search', '')
        cat_filter_form = CategoryFilterForm(request.GET)
        if search_court:
            # Поиск работает / search work
            courts = Courts.objects.filter(Q(plaintiff__icontains=search_court) | Q(defendant__icontains=search_court) | Q(case_number__icontains=search_court) | Q(court_address__icontains=search_court))
    # Фильтрация судебных дел / court list filter         (read_court_users__id=request.user.id)
        if cat_filter_form.is_valid():
            if cat_filter_form.cleaned_data["only_unread_courts"]:
                courts = courts.filter(read_court_users__id=request.user.id)
            if cat_filter_form.cleaned_data["only_my_courts"]:
                courts = courts.filter(Q(author = request.user) | Q(responsible = request.user) | Q(observer = request.user))
            if cat_filter_form.cleaned_data["min_claim_summ"]:
                courts = courts.filter(lawsuit_amount__gte=cat_filter_form.cleaned_data["min_claim_summ"])
            if cat_filter_form.cleaned_data["max_claim_summ"]:
                courts = courts.filter(lawsuit_amount__lte=cat_filter_form.cleaned_data["max_claim_summ"])
            if cat_filter_form.cleaned_data["instance"]:
                courts = courts.filter(instance=cat_filter_form.cleaned_data["instance"])
            if cat_filter_form.cleaned_data["status"]:
                courts = courts.filter(status=cat_filter_form.cleaned_data["status"])
            if cat_filter_form.cleaned_data["jurisdiction"]:
                courts = courts.filter(jurisdiction=cat_filter_form.cleaned_data["jurisdiction"])
            if cat_filter_form.cleaned_data["category"]:
                courts = courts.filter(category=cat_filter_form.cleaned_data["category"])
            if cat_filter_form.cleaned_data["type_proceedings_choises"]:
                courts = courts.filter(type_proceedings_choises=cat_filter_form.cleaned_data["type_proceedings_choises"])
            if cat_filter_form.cleaned_data["court_result"]:
                courts = courts.filter(court_result=cat_filter_form.cleaned_data["court_result"])
    # пагинатор
        paginator = Paginator(courts, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''
        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''
        context = {
            'courts': courts,
            'cat_filter_form':cat_filter_form,
            'page_object': page,
            'is_paginated': is_paginated,
            'next_url': next_url,
            'prev_url': prev_url,
            'page_number': page_number,
            'paginator': paginator,
            'search_court':search_court,
            'unread_courts_count':unread_courts_count,
            'unread_executions_count':unread_executions_count,
        }
        template = 'courts/courts_list.html'
        return render(request, template, context)

# view для страницы отображающей конкретное судебное дело
@login_required
@permission_required('courts.view_courts')
def courts_detail(request, pk):
    # Обект модели конкретного суда
    court = get_object_or_404(Courts, pk=pk)
    # присваиваем значения unread_executions_count и execution_read_count из функции unread_executions_counter_and_var_execution_read_count_logic
    unread_executions_count, execution_read_count = services_executions.unread_executions_counter_and_var_execution_read_count_logic(
        request)
    # присваиваем значения unread_courts_count и courts из функции unread_court_counter_and_var_courts_logic
    unread_courts_count, courts = services_courts.unread_court_counter_and_var_courts_logic(request)
    # форма добавления документов к судебному делу
    courts_documents = CourtDocuments.objects.filter(article=court)
    comments = CommentsCourts.objects.all()
    if request.method == "POST" and 'btnformdocuments' in request.POST:
        form_doc = DocumentForm(request.POST, request.FILES)
        files = request.FILES.getlist('court_ducuments')
        if form_doc.is_valid():
            for file in files:
                file_instance = CourtDocuments(court_ducuments=file, article=court)
                file_instance.save()

        return redirect(courts_detail, pk)
    else:
        form_doc = DocumentForm()
    # форма добавления судебного решения к судебному делу
    courts_judgment = CourtJudgment.objects.filter(article=court)
    if request.method == "POST" and 'btnformjudgment' in request.POST:
        form_judg = JudgmentForm(request.POST, request.FILES)
        files_judg = request.FILES.getlist('court_judjment')
        if form_judg.is_valid():
            for file in files_judg:
                file_instance_judg = CourtJudgment(court_judjment=file, article=court)
                file_instance_judg.save()

        return redirect(courts_detail, pk)
    else:
        form_judg = JudgmentForm()
    # форма добавления комментария к судебному делу
    court_comments = CommentsCourts.objects.filter(article=court)
    if request.method == "POST" and 'btnformcomments' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.article = court
            form.save()
        return redirect(courts_detail, pk)
    else:
        form = CommentForm()
    # при заходе в суд удаляем вошедшего пользователя из списка read_court_users
    court.read_court_users.remove(request.user)
    # последний комментарий суда
    courts_comments_last = court_comments.last()
    all_users = User.objects.all()
    # колличество комментариев в суде
    court_comments_count = int(court_comments.count())
    try:
        if court_comments_count != court.comment_count_model:
            for user_obj in all_users:
                if user_obj != courts_comments_last.author:
                    court.read_court_users.add(user_obj)
            court.comment_count_model = court_comments_count
            court.save()
    except AttributeError:
        pass
# пагинатор
    paginator = Paginator(court_comments, 5)
    page_number = request.GET.get('page', paginator.count)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    obj_type = ContentType.objects.get_for_model(court)
    template = 'courts/courts_detail.html'
    context = {
        'court': court,
        'obj_type':obj_type,'form':form,
        'form_doc':form_doc, 'courts_documents':courts_documents,
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        'page_number': page_number,
        'paginator': paginator,
        'court_comments':court_comments,
        'comments':comments,
        'courts_judgment':courts_judgment,
        'form_judg':form_judg,
        'unread_courts_count':unread_courts_count,
        'unread_executions_count':unread_executions_count,
    }
    return render(request, template, context)


# view для страницы формы изменения конкретного судебного дела
@login_required
@permission_required(['courts.view_courts', 'courts.change_courts'])
def courts_edit(request, pk):
    # присваиваем значения unread_executions_count и execution_read_count из функции unread_executions_counter_and_var_execution_read_count_logic
    unread_executions_count, execution_read_count = services_executions.unread_executions_counter_and_var_execution_read_count_logic(
        request)
    # присваиваем значения unread_courts_count и courts из функции unread_court_counter_and_var_courts_logic
    unread_courts_count, courts = services_courts.unread_court_counter_and_var_courts_logic(request)
    # Обект модели конкретного суда
    courts = get_object_or_404(Courts, pk=pk)
    # форма редактирования судебного дела
    if request.method == "POST":
        form = CourtsFormRedact(request.POST, instance=courts)
        if form.is_valid():
            data = form.cleaned_data['observer']
            court_new = form.save(commit=False)
            if courts.arhive == True:
                courts.arhive_date = datetime.datetime.now()
            courts.last_change_make_user = request.user
            courts.lawsuit_amount = courts.sum_amount_main_prognosis + courts.sum_amount_penalty_agent_prognosis + courts.sum_amount_expertize + courts.sum_of_penalty_prognosis
            courts.total_sum_in_the_case_prognosis = courts.sum_amount_main_prognosis + courts.sum_amount_penalty_agent_prognosis + courts.sum_of_penalty_prognosis + courts.sum_amount_moral_damage_prognosis + courts.state_duty_prognosis + courts.sum_amount_expertize_prognosis
            courts.total_sum_in_the_case = courts.sum_amount_main + courts.sum_amount_penalty_agent + courts.sum_of_penalty + courts.sum_amount_moral_damage + courts.sum_amount_expertize + courts.state_duty
            courts.total_amount_expected_additional = courts.sum_amount_expected_additional + courts.postage_expected_expenses + courts.fare_expected_expenses + courts.other_expected_expenses
            courts.total_amount_additional = courts.sum_amount_additional + courts.postage_expenses + courts.fare_expenses + courts.other_expenses
            courts.save()
            form.save_m2m()
            return redirect('courts_detail', pk=courts.pk)
    else:
        form = CourtsFormRedact(instance=courts)
        template = 'courts/courts_edit.html'
        context = {
            'form': form,
            'courts':courts,
            'unread_executions_count':unread_executions_count,
            'unread_courts_count':unread_courts_count,
        }
        return render(request, template, context)

# view для удаления конкретного судебного дела
@login_required
@permission_required(['courts.view_courts', 'courts.delete_courts'])
def courts_delete(request, pk):
    courts = get_object_or_404(Courts, pk=pk)
    try:
        courts =get_object_or_404(Courts, pk=pk)
        courts.delete()
        return HttpResponseRedirect("/courts")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Суденое дело не найдено</h2>")

# view для удаления комментария в судебном деле
@login_required
@permission_required(['courts_comments.view_courts_comments', 'courts_comments.delete_courts_comments'])
def courts_comments_delete(request, pk):
    courts_comment_delete = get_object_or_404(CommentsCourts, pk=pk)
    courts_comment_delete.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# view для удаления документа в судебном деле
@login_required
@permission_required(['courts_documents.view_courts_documents', 'courts_documents.delete_courts_documents'])
def courts_documents_delete(request, pk):
    courts_document_delete = get_object_or_404(CourtDocuments, pk=pk)
    courts_document_delete.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# view для удаления документа-судебного решения в судебном деле
@login_required
@permission_required(['courts_judgment.view_courts_judgment', 'courts_judgment.delete_courts_judgment'])
def courts_judgment_delete(request, pk):
    courts_judgment_delete = get_object_or_404(CourtJudgment, pk=pk)
    courts_judgment_delete.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# view для страницы судебных дел в архиве
@login_required
@permission_required('courts.view_courts')
def courts_arhive(request):
    # присваиваем значения unread_executions_count и execution_read_count из функции unread_executions_counter_and_var_execution_read_count_logic
    unread_executions_count, execution_read_count = services_executions.unread_executions_counter_and_var_execution_read_count_logic(
        request)
    # присваиваем значения unread_courts_count и courts из функции unread_court_counter_and_var_courts_logic
    unread_courts_count, courts = services_courts.unread_court_counter_and_var_courts_logic(request)
    # поиск архивных судебных дел
    search_court = request.GET.get('search', '')
    if search_court:
        court_in_arhive = Courts.objects.filter(Q(plaintiff__icontains=search_court, arhive=True) | Q(defendant__icontains=search_court, arhive=True) | Q(case_number__icontains=search_court, arhive=True) | Q(court_address__icontains=search_court, arhive=True))
    else:
        court_in_arhive = Courts.objects.filter(arhive=True)
    cat_filter_form = CategoryFilterForm(request.GET)
    # Фильтрация судебных дел
    if cat_filter_form.is_valid():
        if cat_filter_form.cleaned_data["only_my_courts"]:
            court_in_arhive = court_in_arhive.filter(Q(author = request.user) | Q(responsible = request.user) | Q(observer = request.user))
        if cat_filter_form.cleaned_data["min_claim_summ"]:
            court_in_arhive = court_in_arhive.filter(lawsuit_amount__gte=cat_filter_form.cleaned_data["min_claim_summ"])
        if cat_filter_form.cleaned_data["max_claim_summ"]:
            court_in_arhive = court_in_arhive.filter(lawsuit_amount__lte=cat_filter_form.cleaned_data["max_claim_summ"])
        if cat_filter_form.cleaned_data["instance"]:
            court_in_arhive = court_in_arhive.filter(instance=cat_filter_form.cleaned_data["instance"])
        if cat_filter_form.cleaned_data["status"]:
            court_in_arhive = court_in_arhive.filter(status=cat_filter_form.cleaned_data["status"])
        if cat_filter_form.cleaned_data["jurisdiction"]:
            court_in_arhive = court_in_arhive.filter(jurisdiction=cat_filter_form.cleaned_data["jurisdiction"])
        if cat_filter_form.cleaned_data["category"]:
            court_in_arhive = court_in_arhive.filter(category=cat_filter_form.cleaned_data["category"])
        if cat_filter_form.cleaned_data["type_proceedings_choises"]:
            court_in_arhive = court_in_arhive.filter(type_proceedings_choises=cat_filter_form.cleaned_data["type_proceedings_choises"])
        if cat_filter_form.cleaned_data["court_result"]:
            court_in_arhive = court_in_arhive.filter(court_result=cat_filter_form.cleaned_data["court_result"])
    # пагинатор / paginator
    paginator = Paginator(court_in_arhive, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    context = {
        'court_in_arhive': court_in_arhive,
        'cat_filter_form':cat_filter_form,
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        'page_number': page_number,
        'paginator': paginator,
        'search_court':search_court,
        'unread_executions_count':unread_executions_count,
        'unread_courts_count':unread_courts_count,
    }
    template = 'courts/courts_arhive.html'
    return render(request, template, context)


# view страницы - ошибки при отсутвии прав доступа к судебным делам
@login_required
def error_court(request):
    # присваиваем значения unread_executions_count и execution_read_count из функции unread_executions_counter_and_var_execution_read_count_logic
    unread_executions_count, execution_read_count = services_executions.unread_executions_counter_and_var_execution_read_count_logic(
        request)
    # присваиваем значения unread_courts_count и courts из функции unread_court_counter_and_var_courts_logic
    unread_courts_count, courts = services_courts.unread_court_counter_and_var_courts_logic(request)
    error_message = "Внимание, у вас недостаточно прав для перехода к выбранному судебному делу. Для его просмотра, вы должны быть назначены в наблюдатели."
    template = 'courts/court_error.html'
    context = {
        'error_message':error_message,
        'unread_executions_count':unread_executions_count,
        'unread_courts_count':unread_courts_count,
    }
    return render(request, template, context)



