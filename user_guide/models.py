from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django_ulid.models import default, ULIDField
from user_guide.all_validator import phone_mobile_validator, percentage_completion_validator


class DateStamp(models.Model):
    """Временные отметки"""
    created = models.DateTimeField(verbose_name='Дата создания', db_comment='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата изменения', db_comment='Дата изменения', auto_now=True)

    class Meta:
        abstract = True


class Address(DateStamp):
    """Адреса"""
    id_address = ULIDField(verbose_name='id_address', db_comment='id_address', default=default, primary_key=True, editable=False)
    name = models.CharField(verbose_name='Адрес', db_comment='Адрес', max_length=250, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = 'name',

    def __str__(self):
        return self.name


class Office(DateStamp):
    """Кабинет"""
    id_office = ULIDField(verbose_name='id_office', db_comment='id_office', default=default, primary_key=True, editable=False)
    name = models.CharField(verbose_name='Кабинет', db_comment='Кабинет', max_length=250, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
        ordering = 'name',

    def __str__(self):
        return self.name


class Position(DateStamp):
    """Должность"""
    id_position = ULIDField(verbose_name='id_position', db_comment='id_position', default=default, primary_key=True, editable=False)
    name = models.CharField(verbose_name='Должность', db_comment='Должность', max_length=250, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = 'name',

    def __str__(self):
        return self.name


class Subdivision(DateStamp):
    """Подразделение"""
    id_subdivision = ULIDField(verbose_name='id_subdivision', db_comment='id_subdivision', default=default, primary_key=True, editable=False)
    name = models.CharField(verbose_name='Подразделение', db_comment='Подразделение', max_length=250, db_index=True, unique=True)
    description = models.TextField(verbose_name='Описание деятельности', db_comment='Описание деятельности', blank=True, null=True)

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        ordering = 'name',

    def __str__(self):
        return self.name


class Project(DateStamp):
    """Проект"""
    id_project = ULIDField(verbose_name='id_project', db_comment='id_project', default=default, primary_key=True, editable=False)
    name = models.CharField(verbose_name='Проект', db_comment='Проект', max_length=250, db_index=True, unique=True)
    owner = models.CharField(verbose_name='Владелец проекта', db_comment='Владелец проекта', max_length=250)
    description = models.TextField(verbose_name='Описание проекта', db_comment='Описание проекта', blank=True, null=True)
    percentage_completion = models.IntegerField(verbose_name='Процент готовности проекта', db_comment='Процент готовности проекта', validators=[percentage_completion_validator])

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = 'name',

    def __str__(self):
        return self.name


class Note(DateStamp):
    """Заметка"""
    id_note = ULIDField(verbose_name='id_note', db_comment='id_note', default=default, primary_key=True, editable=False)
    name = models.CharField(verbose_name='Заметка', db_comment='Заметка', max_length=250, unique=True)

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = 'name',

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """Сотрудник"""
    id_custom_user = ULIDField(verbose_name='id_custom_user', db_comment='id_custom_user', default=default, primary_key=True, editable=False)
    slug = models.SlugField(verbose_name='slug', db_comment='slug', max_length=255, unique=True, db_index=True, blank=True, null=True)
    username = models.CharField(verbose_name='Логин', db_comment='Логин', max_length=50, db_index=True, unique=True)
    photo = models.ImageField(verbose_name='Фотография', db_comment='Фотография', upload_to='photo_user/', default='photo_user/default/no_photo.png', blank=True, null=True)
    fio = models.CharField(verbose_name='ФИО', db_comment='ФИО', max_length=250, db_index=True, unique=True, blank=True, null=True)
    birthday = models.DateField(verbose_name='Дата рождения', db_comment='Дата рождения', blank=True, null=True)
    biography = models.TextField(verbose_name='Биография', db_comment='Биография', blank=True, null=True)
    email = models.EmailField(verbose_name='Почта', db_comment='Почта', unique=True, blank=True, null=True)
    phone_mobile = models.CharField(verbose_name='Телефон мобильный', db_comment='Телефон мобильный', help_text='Формат +375(00)000-00-00', validators=[phone_mobile_validator], max_length=100, unique=True, blank=True, null=True)
    phone_working = models.CharField(verbose_name='Телефон рабочий', db_comment='Телефон рабочий', help_text='Формат 8(000)000-00-00', max_length=100, blank=True, null=True)
    address = models.ForeignKey(Address, verbose_name='Адрес', db_comment='Адрес', help_text='Адрес рабочего места', on_delete=models.PROTECT, related_name='custom_user_address', blank=True, null=True)
    office = models.ForeignKey(Office, verbose_name='Кабинет', db_comment='Кабинет', help_text='Кабинет рабочего места', on_delete=models.PROTECT, related_name='custom_user_office', blank=True, null=True)
    subdivision = models.ForeignKey(Subdivision, verbose_name='Подразделение', db_comment='Подразделение', on_delete=models.PROTECT, related_name='custom_user_subdivision', blank=True, null=True)
    position = models.ForeignKey(Position, verbose_name='Должность', db_comment='Должность', on_delete=models.PROTECT, related_name='custom_user_position', blank=True, null=True)
    note = models.ForeignKey(Note, verbose_name='Заметка', db_comment='Заметка', on_delete=models.PROTECT, related_name='custom_user_note', blank=True, null=True)
    project = models.ManyToManyField(Project, verbose_name='Проект', related_name='custom_user_project', blank=True)
    cardholder = models.BooleanField(verbose_name='Член профсоюза', db_comment='Член профсоюза', default=False)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = 'fio',
        unique_together = 'fio', 'subdivision', 'position',

    def __str__(self):
        return self.fio or self.username

    def address_info(self):
        if self.office is not None:
            return f'{self.address}, кабинет {self.office}'
        elif self.address is None:
            return 'Нет информации'
        else:
            return f'{self.address}'

    address_info.short_description = 'Адрес рабочего места'

    def clean(self):
        if self.office and not self.address:
            raise ValidationError("Если указан кабинет, укажите поле адрес рабочего места")


class StatusLocation(models.Model):
    """Контроль времени"""
    id_status_location = ULIDField(verbose_name='id_status_location', db_comment='id_status_location', default=default, primary_key=True, editable=False)
    created = models.DateTimeField(verbose_name='Дата и время (входа, выхода)', db_comment='Дата и время (входа, выхода)', auto_now_add=True)
    custom_user = models.ForeignKey(CustomUser, verbose_name='Сотрудник', db_comment='Сотрудник', on_delete=models.PROTECT, related_name='status_location_custom_user', blank=True, null=True)
    camera = models.ForeignKey('Camera', verbose_name='Камера', db_comment='Камера', on_delete=models.PROTECT, related_name='status_location_camera', blank=True, null=True)

    class Meta:
        verbose_name = 'Контроль времени'
        verbose_name_plural = 'Контроль времени'
        ordering = 'created',

    def __str__(self):
        return f''


class Camera(models.Model):
    """Камера"""
    FINDING_CHOICES = (
        (1, 'Вход',),
        (2, 'Выход',),
    )
    id_camera = ULIDField(verbose_name='id_camera', db_comment='id_camera', default=default, primary_key=True, editable=False)
    finding = models.IntegerField(verbose_name='Нахождение', db_comment='Нахождение', choices=FINDING_CHOICES)
    is_active = models.BooleanField(verbose_name='Активный', db_comment='Активный', default=True)
    address = models.ForeignKey(Address, verbose_name='Адрес', db_comment='Адрес', help_text='Адрес рабочего места', on_delete=models.PROTECT, related_name='camera_address', blank=True, null=True)

    class Meta:
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'
        ordering = 'address',
        unique_together = 'finding', 'address',

    def __str__(self):
        return f'{self.get_finding_display()} - ({self.address})'


class Files(DateStamp):
    """Файл"""
    id_files = ULIDField(verbose_name='id_files', db_comment='id_files', default=default, primary_key=True, editable=False)
    files = models.FileField(verbose_name='Файл', db_comment='Файл', upload_to='files/', blank=True, null=True)
    news = models.ForeignKey('News', verbose_name='Новость', db_comment='Новость', on_delete=models.CASCADE, related_name='files_news', blank=True, null=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return f'{self.id_files}'

    @property
    def get_file_size(self):  # Размер файла
        return self.files.size if self.files else 0


class News(DateStamp):
    """Новость"""
    id_news = ULIDField(verbose_name='id_news', db_comment='id_news', default=default, primary_key=True, editable=False)
    name = models.CharField(verbose_name='Название', db_comment='Название', max_length=100)
    description = models.TextField(verbose_name='Описание', db_comment='Описание')
    is_active = models.BooleanField(verbose_name='Опубликована', db_comment='Опубликована', default=True)
    views_count = models.PositiveIntegerField(verbose_name='Просмотров', db_comment='Просмотров', help_text='Количество просмотров)', default=0)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = '-created',

    def __str__(self):
        return self.name


class Setting(DateStamp):
    """Настройки"""
    id_setting = ULIDField(verbose_name='id_setting', db_comment='id_setting', default=default, primary_key=True, editable=False)
    logo = models.ImageField(verbose_name='Логотип организации', db_comment='Логотип организации', upload_to='logo/', default='logo/default/default_logo.png', blank=True, null=True)
    name = models.CharField(verbose_name='Название организации', db_comment='Название организации', help_text='Название организации (краткое)', max_length=100, default='ОРГАНИЗАЦИЯ')
    trade_union_name = models.CharField(verbose_name='Название профсоюза', db_comment='Название профсоюза', max_length=200)
    trade_union_description = models.TextField(verbose_name='Описание профсоюза', db_comment='Описание профсоюза')
    news_page = models.IntegerField(verbose_name='Пагинация новостей', db_comment='Пагинация новостей', default=5)
    subdivision_page = models.IntegerField(verbose_name='Пагинация подразделений', db_comment='Пагинация подразделений', default=5)
    project_page = models.IntegerField(verbose_name='Пагинация проектов', db_comment='Пагинация проектов', default=5)
    book_page = models.IntegerField(verbose_name='Пагинация книг', db_comment='Пагинация книг', default=5)
    trade_union_page = models.IntegerField(verbose_name='Пагинация профсоюзных мероприятий', db_comment='Пагинация профсоюзных мероприятий', default=5)
    time_page = models.IntegerField(verbose_name='Пагинация контроля времени', db_comment='Пагинация контроля времени', default=5)

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return self.name


class Book(DateStamp):
    """Книга"""
    id_book = ULIDField(verbose_name='id_book', db_comment='id_book', default=default, primary_key=True, editable=False)
    logo = models.ImageField(verbose_name='Обложка', db_comment='Обложка', upload_to='book/', default='book/default/default_book.png', blank=True, null=True)
    name = models.CharField(verbose_name='Название', db_comment='Название', help_text='Название книги', max_length=250)
    author = models.CharField(verbose_name='Автор(ы)', db_comment='Автор(ы)', max_length=250)
    files = models.FileField(verbose_name='Файл', db_comment='Файл', upload_to='files/')
    is_active = models.BooleanField(verbose_name='Опубликована', db_comment='Опубликована', default=True)
    download_count = models.PositiveIntegerField(verbose_name='Количество скачиваний', db_comment='Количество скачиваний', default=0)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.name


class TradeUnionPosition(DateStamp):
    """ППО сотрудник"""
    id_trade_union_position = ULIDField(verbose_name='id_trade_union_position', db_comment='id_trade_union_position', default=default, primary_key=True, editable=False)
    custom_user = models.ForeignKey(CustomUser, verbose_name='ППО сотрудник', db_comment='ППО сотрудник', on_delete=models.PROTECT, related_name='trade_union_position_custom_user')
    position = models.ForeignKey(Position, verbose_name='Должность', db_comment='Должность', on_delete=models.PROTECT, related_name='trade_union_position')

    class Meta:
        verbose_name = 'ППО сотрудник'
        verbose_name_plural = 'ППО сотрудники'

    def __str__(self):
        return self.custom_user.fio


class TradeUnionEvent(DateStamp):
    """ППО мероприятие"""
    id_trade_union_event = ULIDField(verbose_name='id_trade_union_event', db_comment='id_trade_union_event', default=default, primary_key=True, editable=False)
    name = models.CharField(verbose_name='Название', db_comment='Название', help_text='Название книги', max_length=250)
    description = models.TextField(verbose_name='Описание', db_comment='Описание')
    is_active = models.BooleanField(verbose_name='Активный', db_comment='Активный', default=True)
    views_count = models.PositiveIntegerField(verbose_name='Просмотров', db_comment='Просмотров', help_text='Количество просмотров)', default=0)

    class Meta:
        verbose_name = 'ППО мероприятие'
        verbose_name_plural = 'ППО мероприятия'

    def __str__(self):
        return self.name


class TradeUnionPhoto(DateStamp):
    """ППО фото мероприятий"""
    id_trade_union_photo = ULIDField(verbose_name='id_trade_union_photo', db_comment='id_trade_union_photo', default=default, primary_key=True, editable=False)
    photo = models.ImageField(verbose_name='Фотография', db_comment='Фотография', upload_to='trade_union_photo/')
    trade_union_event = models.ForeignKey(TradeUnionEvent, verbose_name='Мероприятие', db_comment='Мероприятие', on_delete=models.CASCADE, related_name='trade_union_photo_event', blank=True, null=True)

    class Meta:
        verbose_name = 'ППО фото мероприятий'
        verbose_name_plural = 'ППО фото мероприятий'

    def __str__(self):
        return f'{self.id_trade_union_photo}'
