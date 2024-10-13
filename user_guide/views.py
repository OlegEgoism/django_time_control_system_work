import os
from collections import defaultdict
from datetime import timedelta, datetime
from itertools import groupby
from operator import attrgetter
from urllib.parse import quote
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Subquery, OuterRef, Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from user_guide.forms import (
    CustomUserForm,
    StatusLocationFilterForm,
    ChatForm,
    MessageForm
)
from user_guide.models import (
    CustomUser,
    StatusLocation,
    Setting,
    News,
    Files, Subdivision, Project, Chat
)


def home(request):
    """Главная"""
    config = Setting.objects.first()
    return render(request, template_name='home.html', context={
        'config': config,
    })


def news_list(request):
    """Список новостей"""
    config = Setting.objects.first()
    query = request.GET.get('q')
    news_list = News.objects.filter(is_active=True)
    if query:
        news_list = news_list.filter(Q(name__icontains=query) | Q(description__icontains=query))
    page_size = config.news_page if config else 10
    paginator = Paginator(news_list, page_size)
    page = request.GET.get('page')
    try:
        news_all = paginator.page(page)
    except PageNotAnInteger:
        news_all = paginator.page(1)
    except EmptyPage:
        news_all = paginator.page(paginator.num_pages)
    return render(request, 'news/news_list.html', {
        'config': config,
        'news_all': news_all
    })


def user_list(request):
    """Список сотрудников"""
    config = Setting.objects.first()
    search_query = request.GET.get('q', '')
    query = Q(fio__icontains=search_query) | \
            Q(position__name__icontains=search_query) | \
            Q(email__icontains=search_query) | \
            Q(address__name__icontains=search_query) | \
            Q(phone_mobile__icontains=search_query) | \
            Q(phone_working__icontains=search_query)
    latest_status_subquery = StatusLocation.objects.filter(custom_user=OuterRef('pk')).order_by('-created').values('camera__finding')[:1]
    latest_created_subquery = StatusLocation.objects.filter(custom_user=OuterRef('pk')).order_by('-created').values('created')[:1]
    users = CustomUser.objects.filter(query).annotate(latest_status=Subquery(latest_status_subquery), latest_created=Subquery(latest_created_subquery)).order_by('subdivision', 'position', 'fio')
    grouped_users = {}
    for subdivision, sub_group in groupby(users, key=attrgetter('subdivision')):
        grouped_users[subdivision] = {}
        for position, pos_group in groupby(sub_group, key=attrgetter('position')):
            grouped_users[subdivision][position] = list(pos_group)
    return render(request, template_name='users/user_list.html', context={
        'config': config,
        'grouped_users': grouped_users,
        'search_query': search_query
    })


def subdivision_list(request):
    """Список подразделений с фильтром по названию отдела"""
    config = Setting.objects.first()
    search_query = request.GET.get('q', '')
    query = Q(name__icontains=search_query) | \
            Q(description__icontains=search_query)
    subdivisions = Subdivision.objects.filter(query).annotate(employee_count=Count('custom_user_subdivision')).order_by('name')
    return render(request, 'subdivision_list.html', context={
        'config': config,
        'subdivisions': subdivisions,
        'search_query': search_query
    })


def project_list(request):
    """Список проектов"""
    config = Setting.objects.first()
    search_query = request.GET.get('q', '')
    query = Q(name__icontains=search_query) | \
            Q(owner__icontains=search_query) | \
            Q(description__icontains=search_query)
    projects = Project.objects.filter(query).annotate(employee_count=Count('custom_user_project')).order_by('name')
    return render(request, 'project_list.html', context={
        'config': config,
        'projects': projects,
        'search_query': search_query
    })


# __________________
def user_info(request, slug):
    """Информация о сотруднике"""
    config = Setting.objects.first()
    user = get_object_or_404(CustomUser, slug=slug)
    status_locations = StatusLocation.objects.filter(custom_user=user)
    projects = Project.objects.filter(custom_user_project=user)
    entries = status_locations.filter(camera__finding=1).order_by('created')
    exits = status_locations.filter(camera__finding=2).order_by('created')

    def calculate_total_time(entries, exits):
        total_time = timedelta()
        for entry, exit in zip(entries, exits):
            total_time += exit.created - entry.created
        return total_time

    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    daily_entries = entries.filter(created__gte=start_of_day)
    daily_exits = exits.filter(created__gte=start_of_day)
    daily_time = calculate_total_time(daily_entries, daily_exits)
    monthly_entries = entries.filter(created__gte=start_of_month)
    monthly_exits = exits.filter(created__gte=start_of_month)
    monthly_time = calculate_total_time(monthly_entries, monthly_exits)
    yearly_entries = entries.filter(created__gte=start_of_year)
    yearly_exits = exits.filter(created__gte=start_of_year)
    yearly_time = calculate_total_time(yearly_entries, yearly_exits)

    def format_time(total_time):
        total_seconds = int(total_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours}ч {minutes}м"

    return render(request, template_name='users/user_info.html', context={
        'config': config,
        'user': user,
        'projects': projects,
        'daily_time': format_time(daily_time),
        'monthly_time': format_time(monthly_time),
        'yearly_time': format_time(yearly_time),
    })


def user_edit(request, slug):
    """Редактирование данных сотрудника"""
    config = Setting.objects.first()
    user = get_object_or_404(CustomUser, slug=slug)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)

        # Отладка: Проверьте, что POST-запрос и данные формы отправлены
        print('POST запрос получен:', request.POST)

        if form.is_valid():
            try:
                form.save()  # Сохраняем данные
                messages.success(request, 'Данные сотрудника успешно обновлены')
                return redirect('user_info', slug=user.slug)
            except Exception as e:
                messages.error(request, f'Ошибка сохранения данных: {str(e)}')
        else:
            # Выводим ошибки формы для диагностики
            print('Ошибки формы:', form.errors)
            messages.error(request, f'Ошибки в форме: {form.errors}')
    else:
        form = CustomUserForm(instance=user)

    context = {
        'config': config,
        'form': form,
        'user': user
    }

    return render(request, 'users/user_edit.html', context)


def user_time(request, slug):
    """Контроль рабочего времени"""
    config = Setting.objects.first()
    user = get_object_or_404(CustomUser, slug=slug)
    form = StatusLocationFilterForm(request.GET or None)
    status_locations = StatusLocation.objects.filter(custom_user=user).order_by('-created')
    total_worked_time = timedelta()
    daily_worked_time = defaultdict(timedelta)

    date_from = None
    date_to = None
    if form.is_valid():
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        finding = form.cleaned_data.get('finding')
        address = form.cleaned_data.get('address')
        if date_from:
            status_locations = status_locations.filter(created__gte=date_from)
        if date_to:
            date_to_inclusive = date_to + timedelta(days=1)
            status_locations = status_locations.filter(created__lt=date_to_inclusive)
        if finding:
            status_locations = status_locations.filter(camera__finding=finding)
        if address:
            status_locations = status_locations.filter(camera__address=address)

    paginator = Paginator(status_locations, per_page=config.time_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    enter_times = status_locations.filter(camera__finding=1).order_by('created')
    exit_times = status_locations.filter(camera__finding=2).order_by('created')

    for enter, exit in zip(enter_times, exit_times):
        if exit.created > enter.created:
            worked_duration = exit.created - enter.created
            total_worked_time += worked_duration
            date_key = enter.created.date()
            daily_worked_time[date_key] += worked_duration

    total_seconds = int(total_worked_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f'{hours:02d} часов {minutes:02d} минут {seconds:02d} секунд'

    return render(request, template_name='users/user_time.html', context={
        'config': config,
        'user': user,
        'form': form,
        'page_obj': page_obj,
        'total_worked_time': formatted_time,
    })


def news_info(request, name):
    """Новость"""
    config = Setting.objects.first()
    news = get_object_or_404(News, name=name)
    print('___________________', news.files_news.all())
    news.views_count += 1
    news.save()
    files_with_existence = []
    for file in news.files_news.all():
        file_path = os.path.join(settings.MEDIA_ROOT, str(file.files))
        file_exists = os.path.exists(file_path)
        files_with_existence.append((file, file_exists))
    return render(request, template_name='news/news_info.html', context={
        'config': config,
        'news': news,
        'files_with_existence': files_with_existence,
    })


def news_download_file(request, id_files):
    """Скачивание файла"""
    file_obj = get_object_or_404(Files, id_files=id_files)
    file_path = os.path.join(settings.MEDIA_ROOT, str(file_obj.files))  # Путь к файлу
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file_content:
            response = HttpResponse(file_content.read(), content_type='application/octet-stream')
            file_name = os.path.basename(file_path)
            response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'
            return response
    id_files = file_obj.id_files
    return redirect('news_file_not_found', id_files=id_files)


# def news_file_not_found(request, name):
#     """Если файл не найден"""
#     news = get_object_or_404(News, name=name)
#     return render(request, 'news/news_file_not_found.html', {
#         'news': news,
#     })


@login_required
def chat_list(request):
    """Список чатов для пользователя"""
    chats = Chat.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    return render(request, template_name='chats/chat_list.html', context={
        'chats': chats
    })


@login_required
def create_chat(request):
    """Создание нового чата"""
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender = request.user
            chat.save()
            return redirect('chat_detail', id_chat=chat.id_chat)
    else:
        form = ChatForm(instance=request.user)
    return render(request, template_name='chats/create_chat.html', context={
        'form': form
    })


@login_required
def chat_detail(request, id_chat):
    try:
        chat = Chat.objects.get(id_chat=id_chat)
    except Chat.DoesNotExist:
        raise Http404("Чат не найден.")
    messages = chat.message_chat.all()
    form = MessageForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            return redirect('chat_detail', id_chat=id_chat)
    return render(request, template_name='chats/chat_detail.html', context={
        'chat': chat,
        'messages': messages,
        'form': form
    })
