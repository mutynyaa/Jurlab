from django.shortcuts import render, get_object_or_404
from .models import Executions, ExecutionComments, ExecutionDocuments
from .forms import NewExecutionForm, RedactExecutionForm, ExCommentForm, ExDocumentForm, CategoryFilterForm
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from courts.models import Courts
from django.core.paginator import Paginator, InvalidPage
from profiles.models import Profiles
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from mainpage.models import Supervisor
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist
from courts import services_courts
from . import services_executions
from django.contrib.auth.decorators import login_required

# view для листа исполнительных производств
@login_required
@permission_required('execution.view_executions')
def executions(request):
    # присваиваем значения unread_executions_count и execution_read_count из функции unread_executions_counter_and_var_execution_read_count_logic
    unread_executions_count, executions = services_executions.unread_executions_counter_and_var_execution_read_count_logic(
        request)
    # присваиваем значения unread_courts_count и courts из функции unread_court_counter_and_var_courts_logic
    unread_courts_count, courts = services_courts.unread_court_counter_and_var_courts_logic(request)
    # Поиск испол производств / search executions
    search_ex = request.GET.get('search', '')
    if search_ex:
        # Поиск работает / search work
        executions = Executions.objects.filter(Q(document_nmb__icontains=search_ex) | Q(document_date__icontains=search_ex) | Q(agency__icontains=search_ex) | Q(court__defendant__icontains=search_ex) | Q(court__plaintiff__icontains=search_ex))
    ex_filter_form = CategoryFilterForm(request.GET)
    if ex_filter_form.is_valid():
        if ex_filter_form.cleaned_data["only_my_execution"]:
            executions = executions.filter(Q(author = request.user) | Q(responsible = request.user) | Q(observer = request.user))
        if ex_filter_form.cleaned_data["min_dept_summ"]:
            executions = executions.filter(debt__gte=ex_filter_form.cleaned_data["min_dept_summ"])
        if ex_filter_form.cleaned_data["max_dept_summ"]:
            executions = executions.filter(debt__lte=ex_filter_form.cleaned_data["max_dept_summ"])
        if ex_filter_form.cleaned_data["category"]:
            executions = executions.filter(category=ex_filter_form.cleaned_data["category"])
    # пагинатор / paginator
    paginator = Paginator(executions, 5)
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
    template = 'execution/executions_list.html'
    context = {
        'executions':executions,
        'ex_filter_form':ex_filter_form,
        'search_ex':search_ex,
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        'page_number': page_number,
        'paginator': paginator,
        'unread_executions_count':unread_executions_count,
        'unread_courts_count':unread_courts_count,
    }
    return render(request, template, context)

# view для конкретного исполнительного производства
@login_required
@permission_required('execution.view_executions')
def execution_details(request, pk):
    # присваиваем значения unread_executions_count и execution_read_count из функции unread_executions_counter_and_var_execution_read_count_logic
    unread_executions_count, executions = services_executions.unread_executions_counter_and_var_execution_read_count_logic(request)
    # присваиваем значения unread_courts_count и courts из функции unread_court_counter_and_var_courts_logic
    unread_courts_count, courts = services_courts.unread_court_counter_and_var_courts_logic(request)
    ex_detail_visions = get_object_or_404(Supervisor, id=1)
    ex_detail_vision = ex_detail_visions.ex_author_vision
    execution_detail_var = get_object_or_404(Executions, pk=pk)
    # поправить!!!!!!!!!
    user_is_observer = False
    for item in execution_detail_var.observer.all():
        if item == request.user:
            user_is_observer = True
    if ex_detail_vision == False or request.user.is_staff == True or request.user == execution_detail_var.author or request.user == execution_detail_var.responsible or user_is_observer == True:
        execution_detail = get_object_or_404(Executions, pk=pk)
    else:
         return HttpResponseNotFound("<div align='center'><h2><br /><br /><br />Руководство запретило просмотр не своих исполнительных производств</h2></div>")
    execution_documents = ExecutionDocuments.objects.filter(article=execution_detail)
    if request.method == "POST" and 'btnformdocuments' in request.POST:
        ex_form_doc = ExDocumentForm(request.POST, request.FILES)
        files = request.FILES.getlist('execution_ducuments')
        if ex_form_doc.is_valid():
            for f in files:
                file_instance = ExecutionDocuments(execution_ducuments=f, article=execution_detail_var)
                file_instance.save()

        return redirect(execution_details, pk)
    else:
        ex_form_doc = ExDocumentForm()
    execution_comments = ExecutionComments.objects.filter(article=execution_detail)
    if request.method == "POST" and 'btnformcomments' in request.POST:
        ex_com_form = ExCommentForm(request.POST)
        if ex_com_form.is_valid():
            ex_com_form = ex_com_form.save(commit=False)
            ex_com_form.author = request.user
            ex_com_form.article = execution_detail
            ex_com_form.save()
        return redirect(execution_details, pk)
    else:
        ex_com_form = ExCommentForm()
    # при заходе в суд удаляем вошедшего пользователя из списка read_court_users
    execution_detail_var.read_execution_users.remove(request.user)
    # последний комментарий суда
    execution_comments_last = execution_comments.last()
    all_users = User.objects.all()
    # колличество комментариев в суде
    execution_comments_count = int(execution_comments.count())
    try:
        if execution_comments_count != execution_detail_var.execution_count_model:
            for user_obj in all_users:
                if user_obj != execution_comments_last.author:
                    execution_detail_var.read_execution_users.add(user_obj)
            execution_detail_var.execution_count_model = execution_comments_count
            execution_detail_var.save()
    except AttributeError:
        pass
    paginator = Paginator(execution_comments, 10)
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
    template = 'execution/execution_detail.html'
    context = {
        'execution_detail':execution_detail, 'ex_com_form':ex_com_form,
        'execution_comments':execution_comments, 'paginator':paginator,
        'page_number':page_number, 'page_object': page, 'is_paginated':is_paginated,
        'prev_url':prev_url, 'next_url':next_url, 'execution_documents':execution_documents,
        'ex_form_doc':ex_form_doc, 'ex_detail_vision':ex_detail_vision,
        'unread_executions_count':unread_executions_count,
        'unread_courts_count':unread_courts_count,
    }
    return render(request, template, context)


# view для нового исполнительного производства
@login_required
@permission_required('execution.view_executions', 'execution.add_executions')
def execution_new(request, pk):
    # присваиваем значения unread_executions_count и execution_read_count из функции unread_executions_counter_and_var_execution_read_count_logic
    unread_executions_count, executions = services_executions.unread_executions_counter_and_var_execution_read_count_logic(
        request)
    # присваиваем значения unread_courts_count и courts из функции unread_court_counter_and_var_courts_logic
    unread_courts_count, courts = services_courts.unread_court_counter_and_var_courts_logic(request)
    all_users = User.objects.all()
    court = get_object_or_404(Courts, pk=pk)
    if request.method == "POST":
        form_new_ex = NewExecutionForm(request.POST)
        if form_new_ex.is_valid():
            new_ex = form_new_ex.save(commit=False)
            new_ex.author = request.user
            new_ex.court = court
            new_ex.responsible = court.responsible
            new_ex.save()
            form_new_ex.save_m2m()
            for user_item in all_users:
                new_ex.read_execution_users.add(user_item)
            return redirect('execution_details', pk=new_ex.pk)
    else:
        form_new_ex = NewExecutionForm()
    return render(request, 'execution/execution_new.html', {'form_new_ex': form_new_ex, 'unread_courts_count':unread_courts_count,'unread_executions_count':unread_executions_count,})


# view для нового исполнительного производства
@login_required
@permission_required('execution.view_executions', 'execution.change_executions')
def execution_edit(request, pk):
    # присваиваем значения unread_executions_count и execution_read_count из функции unread_executions_counter_and_var_execution_read_count_logic
    unread_executions_count, executions = services_executions.unread_executions_counter_and_var_execution_read_count_logic(
        request)
    # присваиваем значения unread_courts_count и courts из функции unread_court_counter_and_var_courts_logic
    unread_courts_count, courts = services_courts.unread_court_counter_and_var_courts_logic(request)
    executions = get_object_or_404(Executions, pk=pk)
    if request.method == "POST":
        form_edit_ex = RedactExecutionForm(request.POST, instance=executions)
        if form_edit_ex.is_valid():
            edit_ex = form_edit_ex.save(commit=False)
            edit_ex.save()
            form_edit_ex.save_m2m()
            return redirect('execution_details', pk=edit_ex.pk)
    else:
        form_edit_ex = RedactExecutionForm(instance=executions)
        template = 'execution/execution_edit.html'
        context = {
            'form_edit_ex': form_edit_ex,
            'unread_courts_count':unread_courts_count,
            'unread_executions_count':unread_executions_count,

        }
        return render(request, template, context)


# view для удаления комментариев исполнительного производства
@login_required
@permission_required('execution.view_executions', 'execution.delete_executions')
def ex_comments_delete(request, pk):
    ex_comment_delete = get_object_or_404(ExecutionComments, pk=pk)
    ex_comment_delete.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    
    
# view для удаления исполнительного производства
@login_required
@permission_required('execution.view_executions', 'execution.delete_executions')
def ex_delete(request, pk):
    execution = get_object_or_404(Executions, pk=pk)
    try:
        execution =get_object_or_404(Executions, pk=pk)
        execution.delete()
        return HttpResponseRedirect("/execution")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Суденое дело не найдено</h2>")

# view для удаления исполнительного производства
@login_required
@permission_required('execution.view_executions', 'execution.add_executions')
def ex_arhive(request):
    # присваиваем значения unread_executions_count и execution_read_count из функции unread_executions_counter_and_var_execution_read_count_logic
    unread_executions_count, executions = services_executions.unread_executions_counter_and_var_execution_read_count_logic(
        request)
    # присваиваем значения unread_courts_count и courts из функции unread_court_counter_and_var_courts_logic
    unread_courts_count, courts = services_courts.unread_court_counter_and_var_courts_logic(request)
    executions = Executions.objects.filter(arhive=True)
    # Поиск испол производств в архиве / search executions in arhive
    search_ex = request.GET.get('search', '')
    if search_ex:
        # Поиск работает / search work
        executions = Executions.objects.filter(Q(document_nmb__icontains=search_ex) | Q(document_date__icontains=search_ex) | Q(agency__icontains=search_ex) | Q(court__defendant__icontains=search_ex) | Q(court__plaintiff__icontains=search_ex))
    else:
        # Поиск пустой / search empty
        executions = Executions.objects.filter(arhive=True)
    ex_filter_form = CategoryFilterForm(request.GET)
    if ex_filter_form.is_valid():
        if ex_filter_form.cleaned_data["only_my_execution"]:
            executions = executions.filter(Q(author = request.user) | Q(responsible = request.user) | Q(observer = request.user))
        if ex_filter_form.cleaned_data["min_dept_summ"]:
            executions = executions.filter(debt__gte=ex_filter_form.cleaned_data["min_dept_summ"])
        if ex_filter_form.cleaned_data["max_dept_summ"]:
            executions = executions.filter(debt__lte=ex_filter_form.cleaned_data["max_dept_summ"])
        if ex_filter_form.cleaned_data["category"]:
            executions = executions.filter(category=ex_filter_form.cleaned_data["category"])
    # пагинатор / paginator
    paginator = Paginator(executions, 6)
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
        'executions': executions,
        'ex_filter_form':ex_filter_form,
        'search_ex':search_ex,
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        'page_number': page_number,
        'paginator': paginator,
        'unread_courts_count':unread_courts_count,
        'unread_executions_count':unread_executions_count,

    }
    template = 'execution/executions_arhive.html'
    return render(request, template, context)

    
    
    
# view для удаления исполнительного производства
@login_required
@permission_required('execution.view_executions', 'execution.delete_executions')
def ex_documents_delete(request, pk):
    ex_document_delete = get_object_or_404(ExecutionDocuments, pk=pk)
    ex_document_delete.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
