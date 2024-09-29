import os
from datetime import timedelta, datetime
from itertools import groupby
from operator import attrgetter
from urllib.parse import quote
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Subquery, OuterRef
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from user_guide.forms import CustomUserForm, StatusLocationFilterForm
from user_guide.models import (
    CustomUser,
    StatusLocation,
    Setting,
    News,
    Files
)


def user_list(request):
    """Список пользователей"""
    config = Setting.objects.first()
    search_query = request.GET.get('q', '')

    # Запрос для поиска
    query = Q(fio__icontains=search_query) | \
            Q(phone_mobile__icontains=search_query) | \
            Q(phone_working__icontains=search_query) | \
            Q(email__icontains=search_query) | \
            Q(position__name__icontains=search_query) | \
            Q(address__name__icontains=search_query) | \
            Q(floor__name__icontains=search_query) | \
            Q(office__name__icontains=search_query)

    latest_status_subquery = StatusLocation.objects.filter(custom_user=OuterRef('pk')).order_by('-created').values('camera__finding')[:1]
    latest_created_subquery = StatusLocation.objects.filter(custom_user=OuterRef('pk')).order_by('-created').values('created')[:1]
    users = CustomUser.objects.filter(query).annotate(latest_status=Subquery(latest_status_subquery), latest_created=Subquery(latest_created_subquery)).order_by('subdivision', 'position', 'fio')

    grouped_users = {}
    for subdivision, sub_group in groupby(users, key=attrgetter('subdivision')):
        grouped_users[subdivision] = {}
        for position, pos_group in groupby(sub_group, key=attrgetter('position')):
            grouped_users[subdivision][position] = list(pos_group)

    return render(request, template_name='user_list.html', context={
        'config': config,
        'grouped_users': grouped_users,
        'search_query': search_query
    })


def user_info(request, slug):
    """Информация о пользователе"""
    config = Setting.objects.first()
    user = get_object_or_404(CustomUser, slug=slug)

    # Получаем записи времени входа и выхода
    status_locations = StatusLocation.objects.filter(custom_user=user)
    entries = status_locations.filter(camera__finding=1).order_by('created')
    exits = status_locations.filter(camera__finding=2).order_by('created')

    def calculate_total_time(entries, exits):
        total_time = timedelta()
        for entry, exit in zip(entries, exits):
            total_time += exit.created - entry.created
        return total_time

    # Рассчитываем время за текущий день, месяц и год
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

    # Форматируем время в часы и минуты
    def format_time(total_time):
        total_seconds = int(total_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours}ч {minutes}м"

    return render(request, template_name='user_info.html', context={
        'user': user,
        'config': config,
        'daily_time': format_time(daily_time),
        'monthly_time': format_time(monthly_time),
        'yearly_time': format_time(yearly_time),
    })


def user_edit(request, slug):
    """Редактирование биографии пользователя"""
    config = Setting.objects.first()
    user = get_object_or_404(CustomUser, slug=slug)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_info', slug=user.slug)
    else:
        form = CustomUserForm(instance=user)
    return render(request, template_name='user_edit.html', context={
        'config': config,
        'user': user,
        'form': form
    })


def time_info(request, slug):
    """Отображение информации о рабочем времени с фильтрацией"""
    config = Setting.objects.first()
    user = get_object_or_404(CustomUser, slug=slug)
    form = StatusLocationFilterForm(request.GET or None)
    status_locations = StatusLocation.objects.filter(custom_user=user).order_by('-created')
    total_worked_time = timedelta()

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

    paginator = Paginator(status_locations, per_page=config.time_page)  # Нумерация страниц
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    enter_times = status_locations.filter(camera__finding=1).order_by('created')  # Вход
    exit_times = status_locations.filter(camera__finding=2).order_by('created')  # Выход
    for enter, exit in zip(enter_times, exit_times):
        if exit.created > enter.created:
            total_worked_time += exit.created - enter.created
    total_seconds = int(total_worked_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = f'{hours:02d} часов {minutes:02d} минут {seconds:02d} секунд'
    return render(request, template_name='time_info.html', context={
        'config': config,
        'user': user,
        'form': form,
        'page_obj': page_obj,
        'paginator': paginator,
        'total_worked_time': formatted_time,
    })


# __________________-
def news_list(request):
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
