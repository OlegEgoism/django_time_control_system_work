from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from rangefilter.filters import DateRangeFilter
from user_guide.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm
)
from user_guide.models import (
    StatusLocation,
    Address,
    Subdivision,
    Position,
    CustomUser,
    Note,
    Camera,
    Setting,
    Files,
    News,
    Office,
    Project, Chat, Message
)


class AddressFilter(AutocompleteFilter):
    title = 'Адрес рабочего места'
    field_name = 'address'


class SubdivisionFilter(AutocompleteFilter):
    title = 'Подразделение'
    field_name = 'subdivision'


class ProjectFilter(AutocompleteFilter):
    title = 'Проект'
    field_name = 'project'


class PositionFilter(AutocompleteFilter):
    title = 'Должность'
    field_name = 'position'


class NoteFilter(AutocompleteFilter):
    title = 'Заметка'
    field_name = 'note'


class CustomUserFilter(AutocompleteFilter):
    title = 'Сотрудник'
    field_name = 'custom_user'


class CameraFilter(AutocompleteFilter):
    title = 'Камера'
    field_name = 'camera'


# ______________________________________________________
class StatusLocationInline(admin.TabularInline):
    """Контроль времени"""
    model = StatusLocation
    extra = 0
    classes = ['collapse']
    readonly_fields = 'created', 'camera'
    can_delete = False  # Запретить удаление объектов


class FilesInline(admin.TabularInline):
    """Файлы"""
    model = Files
    extra = 1
    max_num = 10  # Лимит до 10 файлов


# ______________________________________________________
@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    """Кабинет рабочего места"""
    list_display = 'name', 'created', 'updated', 'count_position',
    readonly_fields = 'created', 'updated',
    search_fields = 'name',
    search_help_text = 'Поиск по кабинету рабочего места'
    list_per_page = 20

    def count_position(self, obj):
        return obj.custom_user_office.count()

    count_position.short_description = 'Количество сотрудников'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Адрес рабочего места"""
    list_display = 'name', 'created', 'updated', 'count_position',
    readonly_fields = 'created', 'updated',
    search_fields = 'name',
    search_help_text = 'Поиск по адресу'
    ordering = 'name',
    list_per_page = 20

    def count_position(self, obj):
        return obj.custom_user_address.count()

    count_position.short_description = 'Количество сотрудников'


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Должность"""
    list_display = 'name', 'created', 'updated', 'count_position',
    readonly_fields = 'created', 'updated',
    search_fields = 'name',
    search_help_text = 'Поиск по должности'
    ordering = 'name',
    list_per_page = 20

    def count_position(self, obj):
        return obj.custom_user_position.count()

    count_position.short_description = 'Количество сотрудников'


@admin.register(Subdivision)
class SubdivisionAdmin(admin.ModelAdmin):
    """Подразделение"""
    list_display = 'name', 'short_question', 'count_subdivision', 'created', 'updated',
    readonly_fields = 'created', 'updated',
    search_fields = 'name', 'short_question',
    search_help_text = 'Поиск по подразделению и описании деятельности'
    ordering = 'name',
    list_per_page = 20

    def count_subdivision(self, obj):
        return obj.custom_user_subdivision.count()

    count_subdivision.short_description = 'Количество сотрудников'

    def short_question(self, obj):
        len_str = 200
        return obj.description[:len_str] + "..." if len(obj.description) > len_str else obj.description

    short_question.short_description = 'Описание деятельности'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Проекты"""
    list_display = 'name', 'short_question', 'owner', 'percentage_completion', 'count_project', 'created', 'updated',
    readonly_fields = 'created', 'updated',
    search_fields = 'name', 'owner',
    list_filter = 'owner',
    search_help_text = 'Поиск по названию и владельцу проекта'
    ordering = 'name',
    list_per_page = 20

    def count_project(self, obj):
        return obj.custom_user_project.count()

    count_project.short_description = 'Количество сотрудников'

    def short_question(self, obj):
        len_str = 200
        return obj.description[:len_str] + "..." if len(obj.description) > len_str else obj.description

    short_question.short_description = 'Описание деятельности'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Заметка"""
    list_display = 'name', 'count_note',
    readonly_fields = 'created', 'updated',
    search_fields = 'name',
    search_help_text = 'Поиск по заметкам'
    ordering = 'name',
    list_per_page = 20

    def count_note(self, obj):
        return obj.custom_user_note.count()

    count_note.short_description = 'Количество сотрудников'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Сотрудник"""

    # Подключаем кастомные формы для создания и изменения пользователя
    add_form = CustomUserCreationForm  # Форма для создания
    form = CustomUserChangeForm  # Форма для изменения
    model = CustomUser

    fieldsets = (
        (None, {
            'fields': ('username', 'password',)}),
        ('РАЗРЕШЕНИЯ', {
            'classes': ('collapse',),
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined',)}),
        ('ЛИЧНЫЕ ДАННЫЕ', {
            'fields': (
                'preview_photo', 'photo', 'fio', 'slug', 'birthday', 'biography', 'email', 'phone_mobile',
                'phone_working',
                'address', 'office', 'note', 'position', 'subdivision', 'project',)},),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'fio', 'slug', 'password1', 'password2'),
        }),
    )
    list_display = 'username', 'preview_photo', 'fio', 'phone_mobile', 'phone_working', 'note', 'subdivision', 'position', 'address_info', 'is_active',
    list_filter = 'is_active', NoteFilter, SubdivisionFilter, PositionFilter, AddressFilter, ProjectFilter
    readonly_fields = 'last_login', 'date_joined', 'preview_photo',
    search_fields = 'username', 'fio', 'phone_mobile', 'phone_working', 'position', 'subdivision',
    search_help_text = 'Поиск по логину, имени пользователя и номеру телефона, должности, подразделению'
    prepopulated_fields = {'slug': ('fio',)}
    inlines = StatusLocationInline,
    list_select_related = 'address', 'office', 'note', 'position', 'subdivision',
    list_per_page = 20

    def preview_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="80" height="80" style="border-radius: 50%;" />')
        else:
            return 'Нет фотографии'

    preview_photo.short_description = 'Фотография'

    def save_model(self, request, obj, form, change):
        """Проверка, есть ли еще один пользователь с таким же адресом электронной почты"""
        if obj.email:
            if CustomUser.objects.filter(email=obj.email).exclude(pk=obj.pk).exists():
                self.message_user(request, "Этот адрес электронной почты уже связан с другим аккаунтом", level='ERROR')
                return
        super().save_model(request, obj, form, change)


@admin.register(StatusLocation)
class StatusLocationAdmin(admin.ModelAdmin):
    """Контроль времени"""
    fields = 'camera', 'custom_user', 'created',
    list_display = 'created', 'camera', 'custom_user',
    list_filter = ("created", DateRangeFilter), CustomUserFilter, CameraFilter,
    readonly_fields = 'created',
    date_hierarchy = 'created'
    search_fields = 'custom_user__fio', 'camera__address__name'
    search_help_text = 'Поиск по ФИО и адресу местонахождения камеры'
    ordering = '-created',
    list_per_page = 20


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    """Камера"""
    fields = 'finding', 'address', 'is_active',
    list_display = '__str__', 'id_camera', 'is_active',
    list_filter = 'is_active', 'finding', AddressFilter,
    search_fields = 'address__name',
    search_help_text = 'Поиск по адресу местонахождения камеры'
    list_per_page = 20


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Новость"""
    list_display = 'name', 'views_count', 'file_count', 'is_active', 'created', 'updated',
    list_editable = 'is_active',
    list_filter = 'is_active', ('created', DateRangeFilter),
    readonly_fields = 'created', 'updated', 'views_count',
    inlines = FilesInline,
    search_fields = 'name', 'description',
    search_help_text = 'Поиск по названию новости и описанию'
    date_hierarchy = 'created'
    list_per_page = 20
    ordering = 'created',

    def file_count(self, obj):
        if obj.files_news.count() == 0:
            return 'Нет файлов'
        else:
            return obj.files_news.count()

    file_count.short_description = 'Количество файлов'


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """Настройки"""
    fields = 'preview_logo', 'logo', 'name', 'news_page', 'time_page',
    list_display = 'name', 'preview_logo', 'created', 'updated',
    readonly_fields = 'created', 'updated', 'preview_logo',

    def preview_logo(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="100" height="100" />')
        else:
            return 'Нет логотипа'

    preview_logo.short_description = 'Логотип организации'

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return True


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
