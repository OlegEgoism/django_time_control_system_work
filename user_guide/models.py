from django.contrib.auth.models import AbstractUser
from django.db import models
from django_ulid.models import default, ULIDField


class DateStamp(models.Model):
    """Отметка даты"""
    created = models.DateTimeField(verbose_name='Дата и время создания', db_comment='Дата и время создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата и время изменения', db_comment='Дата и время изменения', auto_now=True)

    class Meta:
        abstract = True


class Address(DateStamp):
    """Адрес рабочего места"""
    id_address = ULIDField(verbose_name='id_address', db_comment='id_address', default=default, primary_key=True, editable=False)
    name = models.CharField(verbose_name='Адрес рабочего места', db_comment='Адрес рабочего места', max_length=250, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Адрес рабочего места'
        verbose_name_plural = 'Адреса рабочего места'
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

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
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
    username = models.CharField(verbose_name='Логин', db_comment='Логин', max_length=50, db_index=True, unique=True)
    photo = models.ImageField(verbose_name='Фотография', db_comment='Фотография', upload_to='photo_user/', blank=True, null=True)
    fio = models.CharField(verbose_name='ФИО', db_comment='ФИО', max_length=250, db_index=True, unique=True, blank=True, null=True)
    birthday = models.DateField(verbose_name='Дата рождения', db_comment='Дата рождения', blank=True, null=True)
    biography = models.TextField(verbose_name='Биография', db_comment='Биография', blank=True, null=True)
    email = models.EmailField(verbose_name='Почта', db_comment='Почта', unique=True, blank=True, null=True)
    phone_mobile = models.CharField(verbose_name='Телефон мобильный', db_comment='Телефон мобильный', help_text='Формат 375(00)000-00-00', max_length=100, unique=True, blank=True, null=True)
    phone_working = models.CharField(verbose_name='Телефон рабочий', db_comment='Телефон рабочий', help_text='Формат 8(000)000-00-00', max_length=100, blank=True, null=True)
    address = models.ForeignKey(Address, verbose_name='Адрес рабочего места', db_comment='Адрес рабочего места', on_delete=models.PROTECT, related_name='custom_user_address', blank=True, null=True)
    subdivision = models.ForeignKey(Subdivision, verbose_name='Подразделение', db_comment='Подразделение', on_delete=models.PROTECT, related_name='custom_user_subdivision', blank=True, null=True)
    position = models.ForeignKey(Position, verbose_name='Должность', db_comment='Должность', on_delete=models.PROTECT, related_name='custom_user_position', blank=True, null=True)
    note = models.ForeignKey(Note, verbose_name='Заметка', db_comment='Заметка', on_delete=models.PROTECT, related_name='custom_user_note', blank=True, null=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = 'fio',
        unique_together = 'fio', 'subdivision', 'position',

    def __str__(self):
        return self.fio or self.username


class StatusLocation(models.Model):
    """Контроль времени"""
    id_status_location = ULIDField(verbose_name='id_status_location', db_comment='id_status_location', default=default, primary_key=True, editable=False)
    created = models.DateTimeField(verbose_name='Дата и время (входа, выхода)', db_comment='Дата и время', auto_now_add=True)
    custom_user = models.ForeignKey(CustomUser, verbose_name='Сотрудник', db_comment='Сотрудник', on_delete=models.PROTECT, null=True, blank=True, related_name='status_location_custom_user')
    camera = models.ForeignKey('Camera', verbose_name='Камера', db_comment='Камера', on_delete=models.PROTECT, null=True, blank=True, related_name='status_location_camera')

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
    address = models.ForeignKey(Address, verbose_name='Адрес рабочего места', db_comment='Адрес рабочего места', on_delete=models.PROTECT, null=True, blank=True, related_name='camera_address')

    class Meta:
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'
        ordering = 'address',
        unique_together = 'finding', 'address',

    def __str__(self):
        return f'{self.get_finding_display()} - ({self.address})'


class Setting(DateStamp):
    """Настройки сайта"""
    id_setting = ULIDField(verbose_name='id_setting', db_comment='id_setting', default=default, primary_key=True, editable=False)
    logo = models.ImageField(verbose_name='Логотип организации', db_comment='Логотип организации', upload_to='logo/', blank=True, null=True)
    name = models.CharField(verbose_name='Название организации', db_comment='Название организации', max_length=250)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return self.name
