import math
import os
from collections import defaultdict
from datetime import timedelta, datetime
from itertools import groupby
from operator import attrgetter
from pyexpat.errors import messages
from urllib.parse import quote
from django.http import JsonResponse, Http404, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import (
    authenticate,
    login
)
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage
)
from django.db.models import (
    Q,
    Subquery,
    OuterRef,
    Count
)
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from user_guide.forms import (
    CustomUserForm,
    StatusLocationFilterForm, OrganizerForm
)
from user_guide.models import (
    CustomUser,
    StatusLocation,
    Setting,
    News,
    Files,
    Subdivision,
    Project,
    Book,
    TradeUnionPosition,
    TradeUnionPhoto,
    TradeUnionEvent, Room, Message, Organizer
)


# TODO Главная
def home(request):
    """Главная"""
    config = Setting.objects.first()
    users = CustomUser.objects.filter(is_active=True)
    return render(request, template_name='home.html', context={
        'config': config,
        'users': users,
    })


# TODO Новости
def news_list(request):
    """Новости"""
    config = Setting.objects.first()
    page_size = config.news_page
    search_query = request.GET.get('q', '')
    query = Q(name__icontains=search_query) | \
            Q(description__icontains=search_query)
    news = News.objects.filter(is_active=True).filter(query)
    paginator = Paginator(news, page_size)
    page = request.GET.get('page')
    try:
        news_all = paginator.page(page)
    except PageNotAnInteger:
        news_all = paginator.page(1)
    except EmptyPage:
        news_all = paginator.page(paginator.num_pages)
    return render(request, template_name='news/news_list.html', context={
        'config': config,
        'news_all': news_all,
        'search_query': search_query
    })


def news_info(request, name):
    """Новость"""
    config = Setting.objects.first()
    news = get_object_or_404(News, name=name)
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


# TODO Сотрудники
def user_list(request):
    """Сотрудники"""
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


def user_info(request, slug):
    """Информация о сотруднике"""
    config = Setting.objects.first()
    user = get_object_or_404(CustomUser, slug=slug)
    status_locations = StatusLocation.objects.filter(custom_user=user)
    projects = Project.objects.filter(custom_user_project=user)
    entries = status_locations.filter(camera__finding=1).order_by('created')
    exits = status_locations.filter(camera__finding=2).order_by('created')
    is_owner_or_admin = request.user == user or request.user.is_staff

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
        'is_owner_or_admin': is_owner_or_admin,
    })


def user_edit(request, slug):
    """Редактирование данных сотрудника"""
    config = Setting.objects.first()
    user = get_object_or_404(CustomUser, slug=slug)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно обновлены!')
            return redirect('user_info', slug=user.slug)
    else:
        form = CustomUserForm(instance=user)
    return render(request, template_name='users/user_edit.html', context={
        'config': config,
        'form': form,
        'user': user
    })


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


# TODO Подразделения
def subdivision_list(request):
    """Подразделения"""
    config = Setting.objects.first()
    page_size = config.subdivision_page
    search_query = request.GET.get('q', '')
    query = Q(name__icontains=search_query) | \
            Q(description__icontains=search_query)
    subdivisions = Subdivision.objects.filter(query).annotate(employee_count=Count('custom_user_subdivision')).order_by('name')
    paginator = Paginator(subdivisions, page_size)
    page = request.GET.get('page')
    try:
        subdivisions_page = paginator.page(page)
    except PageNotAnInteger:
        subdivisions_page = paginator.page(1)
    except EmptyPage:
        subdivisions_page = paginator.page(paginator.num_pages)
    return render(request, template_name='subdivision_list.html', context={
        'config': config,
        'subdivisions': subdivisions_page,
        'search_query': search_query
    })


# TODO Проекты
def project_list(request):
    """Проекты"""
    config = Setting.objects.first()
    page_size = config.project_page
    search_query = request.GET.get('q', '')
    query = Q(name__icontains=search_query) | \
            Q(owner__icontains=search_query) | \
            Q(description__icontains=search_query)
    projects = Project.objects.filter(query).annotate(employee_count=Count('custom_user_project')).order_by('name')
    paginator = Paginator(projects, page_size)
    page = request.GET.get('page')
    try:
        projects_page = paginator.page(page)
    except PageNotAnInteger:
        projects_page = paginator.page(1)
    except EmptyPage:
        projects_page = paginator.page(paginator.num_pages)
    return render(request, template_name='projects/project_list.html', context={
        'config': config,
        'projects': projects_page,
        'search_query': search_query
    })


def project_info(request, id_project):
    """Отображение информации о проекте и списке сотрудников"""
    config = Setting.objects.first()
    project = Project.objects.annotate(employee_count=Count('custom_user_project')).get(id_project=id_project)
    employees = CustomUser.objects.filter(project=project)
    return render(request, template_name="projects/project_info.html", context={
        'config': config,
        'project': project,
        'employees': employees,
    })



# TODO Книги
def book_list(request):
    """Книги"""
    config = Setting.objects.first()
    page_size = config.book_page
    search_query = request.GET.get('q', '')
    query = Q(author__icontains=search_query) | Q(name__icontains=search_query)
    books = Book.objects.filter(query).order_by('name')
    paginator = Paginator(books, page_size)
    page = request.GET.get('page')
    try:
        books_page = paginator.page(page)
    except PageNotAnInteger:
        books_page = paginator.page(1)
    except EmptyPage:
        books_page = paginator.page(paginator.num_pages)
    for book in books_page:
        if book.files and os.path.exists(book.files.path):
            book.file_size = convert_size(book.files.size)
        else:
            book.file_size = "Файл не найден"
    return render(request, template_name='book.html', context={
        'config': config,
        'books': books_page,
        'search_query': search_query
    })


def convert_size(size_bytes):
    """Преобразует размер в читаемый формат"""
    if size_bytes == 0:
        return "0 Bytes"
    size_name = ("Bytes", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def book_download_file(request, id_book):
    """Скачивание книги"""
    book = get_object_or_404(Book, id_book=id_book)
    if not book.files or not os.path.exists(book.files.path):
        raise Http404("Файл не найден или был удален.")
    response = HttpResponse(book.files, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{book.name}.pdf"'
    return response


def book_download_count(request, id_book):
    """Счетчик скачиваний книги"""
    book = get_object_or_404(Book, id_book=id_book)
    book.download_count += 1
    book.save()
    return JsonResponse({'new_count': book.download_count})


# TODO Профсоюз
def trade_union(request):
    """Профсоюз"""
    config = Setting.objects.first()
    page_size = config.trade_union_page
    search_query = request.GET.get('q', '')
    query = Q(name__icontains=search_query) | Q(description__icontains=search_query)
    trade_union_events = TradeUnionEvent.objects.filter(is_active=True).filter(query).order_by('-created')
    paginator = Paginator(trade_union_events, page_size)
    page = request.GET.get('page')
    try:
        trade_union_events_page = paginator.page(page)
    except PageNotAnInteger:
        trade_union_events_page = paginator.page(1)
    except EmptyPage:
        trade_union_events_page = paginator.page(paginator.num_pages)
    trade_union_positions = TradeUnionPosition.objects.select_related('custom_user', 'position').all()
    photo_count = TradeUnionPhoto.objects.filter(trade_union_event__is_active=True).count()
    return render(request, template_name='trade_union/trade_union.html', context={
        'config': config,
        'trade_union_positions': trade_union_positions,
        'trade_union_events': trade_union_events_page,
        'photo_count': photo_count,
        'search_query': search_query
    })


def trade_union_event(request, name):
    """Профсоюзное мероприятие"""
    config = Setting.objects.first()
    event = get_object_or_404(TradeUnionEvent, name=name)
    event.views_count += 1
    event.save()
    photos = TradeUnionPhoto.objects.filter(trade_union_event=event)
    return render(request, template_name='trade_union/trade_union_event_detail.html', context={
        'config': config,
        'event': event,
        'photos': photos,
    })


# TODO Авторизация(Вход/Выход)
def user_login(request):
    """Вход"""
    config = Setting.objects.first()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Перенаправление после успешного входа
        else:
            error_message = 'Неверный логин или пароль'
            return render(request, 'login.html', {'config': config, 'error_message': error_message})
    return render(request, template_name='login.html', context={
        'config': config
    })


def user_logout(request):
    """Выход"""
    logout(request)
    return redirect('/')


# TODO Чат
def rooms(request):
    """Список чатов"""
    config = Setting.objects.first()
    if request.user.is_superuser:
        rooms = Room.objects.filter(is_active=True).annotate(user_count=Count('message_content__user', distinct=True))
    else:
        rooms = Room.objects.filter(is_active=True, custom_user_room=request.user).annotate(user_count=Count('message_content__user', distinct=True))
    return render(request, template_name="chat/rooms.html", context={
        'config': config,
        'rooms': rooms
    })


def room(request, slug):
    """Чат"""
    config = Setting.objects.first()
    try:
        room_instance = Room.objects.get(slug=slug)
        room_name = room_instance.name
        messages = Message.objects.filter(room=room_instance)
        created_date = room_instance.created
        unique_users = CustomUser.objects.filter(message_user__room=room_instance).distinct()
    except Room.DoesNotExist:
        raise Http404("Чат не найден")
    return render(request, template_name="chat/room.html", context={
        'config': config,
        'room_name': room_name,
        'messages': messages,
        'created_date': created_date,
        'unique_users': unique_users
    })


def organizer(request):
    """Органайзер"""
    config = Setting.objects.first()
    events = Organizer.objects.all()
    return render(request, template_name="organizer/calendar.html", context={
        'config': config,
        'events': events,
    })


def add_event(request):
    """Добавить мероприятие"""
    config = Setting.objects.first()
    if request.method == 'POST':
        form = OrganizerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Мероприятие успешно добавлено.')
            return redirect('organizer')  # Замените 'organizer' на имя URL страницы календаря
    else:
        form = OrganizerForm()
    return render(request, template_name='organizer/add_event.html', context={
        'config': config,
        'form': form
    })


def edit_event(request, event_id):
    """Редактирование события"""
    config = Setting.objects.first()
    event = get_object_or_404(Organizer, id=event_id)
    if request.method == 'POST':
        form = OrganizerForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('organizer')
    else:
        form = OrganizerForm(instance=event)
    return render(request, template_name='organizer/edit_event.html', context={
        'config': config,
        'form': form,
        'event':event
    })


def delete_event(request, event_id):
    """Удалить мероприятие"""
    event = get_object_or_404(Organizer, id=event_id)
    event.delete()
    messages.success(request, 'Мероприятие успешно удалено.')
    return redirect('organizer')  # Перенаправление на страницу календаря
