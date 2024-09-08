from datetime import timedelta, datetime
from itertools import groupby
from operator import attrgetter
from django.db.models import Q, Subquery, OuterRef
from django.shortcuts import render, get_object_or_404
from user_guide.models import (
    CustomUser,
    StatusLocation,
    Setting
)


def index(request):
    return render(request, 'index.html')


def user_list(request):
    """Список пользователей с возможностью поиска"""
    settings = Setting.objects.first()
    search_query = request.GET.get('q', '')

    # Создаем запрос для поиска
    query = Q(fio__icontains=search_query) | \
            Q(phone_mobile__icontains=search_query) | \
            Q(phone_working__icontains=search_query) | \
            Q(email__icontains=search_query) | \
            Q(position__name__icontains=search_query)

    latest_status_subquery = StatusLocation.objects.filter(
        custom_user=OuterRef('pk')
    ).order_by('-created').values('camera__finding')[:1]

    latest_created_subquery = StatusLocation.objects.filter(
        custom_user=OuterRef('pk')
    ).order_by('-created').values('created')[:1]

    users = CustomUser.objects.filter(query).annotate(
        latest_status=Subquery(latest_status_subquery),
        latest_created=Subquery(latest_created_subquery)
    ).order_by('subdivision', 'position', 'fio')

    grouped_users = {}
    for subdivision, sub_group in groupby(users, key=attrgetter('subdivision')):
        grouped_users[subdivision] = {}
        for position, pos_group in groupby(sub_group, key=attrgetter('position')):
            grouped_users[subdivision][position] = list(pos_group)

    return render(request, template_name='home.html', context={
        'settings': settings,
        'grouped_users': grouped_users,
        'search_query': search_query
    })


# def user_info(request, fio):
#     """Информация о пользователе"""
#     settings = Setting.objects.first()
#     user = get_object_or_404(CustomUser, fio=fio)
#     return render(request, template_name='user_info.html', context={
#         'user': user,
#         'settings': settings
#     })


# def user_info(request, fio):
#     """Информация о пользователе"""
#     settings = Setting.objects.first()
#     user = get_object_or_404(CustomUser, fio=fio)
#     status_locations = StatusLocation.objects.filter(custom_user=user)
#     entries = status_locations.filter(camera__finding=1).order_by('created')
#     exits = status_locations.filter(camera__finding=2).order_by('created')
#
#     total_time = timedelta()
#     for entry, exit in zip(entries, exits):
#         total_time += exit.created - entry.created
#
#     return render(request, template_name='user_info.html', context={
#         'user': user,
#         'settings': settings,
#         'total_time': total_time
#     })


# def user_info(request, fio):
#     """Информация о пользователе"""
#     settings = Setting.objects.first()
#     user = get_object_or_404(CustomUser, fio=fio)
#
#     # Получаем записи времени входа и выхода
#     status_locations = StatusLocation.objects.filter(custom_user=user)
#     entries = status_locations.filter(camera__finding=1).order_by('created')
#     exits = status_locations.filter(camera__finding=2).order_by('created')
#
#     # Рассчитываем общее отработанное время
#     total_time = timedelta()
#     for entry, exit in zip(entries, exits):
#         total_time += exit.created - entry.created
#
#     # Форматируем время в часы и минуты
#     total_seconds = int(total_time.total_seconds())
#     hours, remainder = divmod(total_seconds, 3600)
#     minutes, seconds = divmod(remainder, 60)
#     formatted_time = f"{hours}ч {minutes}м"
#
#     return render(request, template_name='user_info.html', context={
#         'user': user,
#         'settings': settings,
#         'total_time': formatted_time
#     })





def user_info(request, fio):
    """Информация о пользователе"""
    settings = Setting.objects.first()
    user = get_object_or_404(CustomUser, fio=fio)

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
        'settings': settings,
        'daily_time': format_time(daily_time),
        'monthly_time': format_time(monthly_time),
        'yearly_time': format_time(yearly_time),
    })
