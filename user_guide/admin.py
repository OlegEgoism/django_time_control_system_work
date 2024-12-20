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
    Project, Book, TradeUnionPosition, TradeUnionPhoto, TradeUnionEvent, Room, Message
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
    max_num = 10  # Лимит до файлов


class TradeUnionPhotoInline(admin.TabularInline):
    """Файлы"""
    model = TradeUnionPhoto
    extra = 0
    max_num = 50  # Лимит до файлов
    readonly_fields = 'preview_photo',
    fields = 'preview_photo', 'photo',

    def preview_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100"/>')
        else:
            return 'Нет фото'

    preview_photo.short_description = 'Фотография мероприятий'


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
        if obj.description:
            return obj.description[:len_str] + "..." if len(obj.description) > len_str else obj.description
        return "Информация не заполнена"

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
        if obj.description:
            return obj.description[:len_str] + "..." if len(obj.description) > len_str else obj.description
        return "Информация не заполнена"

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

    # Подключаем кастомные формы для создания и изменения сотрудника
    add_form = CustomUserCreationForm  # Форма для создания
    form = CustomUserChangeForm  # Форма для изменения
    model = CustomUser

    fieldsets = (
        (None, {
            'fields': ('username', 'password',)}),

        ('ЛИЧНЫЕ ДАННЫЕ', {
            'fields': (
                'preview_photo', 'photo', 'fio', 'slug', 'birthday', 'biography', 'email', 'phone_mobile', 'phone_working',
                'address', 'office', 'note', 'position', 'subdivision', 'project', 'room', 'cardholder',)},),
        ('РАЗРЕШЕНИЯ', {
            # 'classes': ('collapse',),
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            # 'classes': ('wide',),
            'fields': ('username', 'email', 'fio', 'slug', 'password1', 'password2'),
        }),
    )
    list_display = 'username', 'preview_photo', 'fio', 'phone_mobile', 'note', 'subdivision', 'position', 'address_info', 'is_active', 'cardholder',
    list_filter = 'cardholder', 'is_active', NoteFilter, SubdivisionFilter, PositionFilter, AddressFilter, ProjectFilter
    readonly_fields = 'last_login', 'date_joined', 'preview_photo',
    search_fields = 'username', 'fio', 'phone_mobile', 'phone_working', 'position', 'subdivision',
    search_help_text = 'Поиск по логину, имени сотрудника и номеру телефона, должности, подразделению'
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
        """Проверка, есть ли еще один сотрудник с таким же адресом электронной почты"""
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
    fields = 'preview_logo', 'logo', 'name', 'info_description', 'trade_union_name', 'trade_union_description', 'news_page', 'subdivision_page', 'project_page', 'book_page', 'trade_union_page', 'time_page',
    list_display = 'name', 'created', 'updated',
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


@admin.register(Book)
class TradeUnionAdmin(admin.ModelAdmin):
    """Книги"""
    list_display = 'author', 'name', 'preview_logo', 'download_count', 'created', 'updated',
    readonly_fields = 'preview_logo', 'download_count', 'created', 'updated',
    fields = 'author', 'name', 'preview_logo', 'logo', 'files', 'is_active', 'download_count', 'created', 'updated',
    search_fields = 'author', 'name',
    search_help_text = 'Поиск по названию автору и названию'
    date_hierarchy = 'created'
    list_per_page = 20
    ordering = 'created',

    def preview_logo(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="100" height="100"/>')
        else:
            return 'Нет обложки'

    preview_logo.short_description = 'Обложка'


@admin.register(TradeUnionPosition)
class TradeUnionPositionAdmin(admin.ModelAdmin):
    """Сотрудники профсоюза"""
    list_display = 'custom_user', 'position', 'created', 'updated',


@admin.register(TradeUnionEvent)
class TradeUnionEventAdmin(admin.ModelAdmin):
    """Сотрудники профсоюза"""
    list_display = 'name', 'short_description', 'is_active', 'trade_union_photo_count', 'created', 'updated',
    list_editable = 'is_active',
    list_filter = 'is_active',
    search_fields = 'name',
    search_help_text = 'Поиск по названию и описанию'
    date_hierarchy = 'created'
    list_per_page = 20
    ordering = 'created',
    inlines = TradeUnionPhotoInline,

    def short_description(self, obj):
        len_str = 200
        if obj.description:
            return obj.description[:len_str] + "..." if len(obj.description) > len_str else obj.description
        return "Информация не заполнена"

    short_description.short_description = 'Описание мероприятия'

    def trade_union_photo_count(self, obj):
        if obj.trade_union_photo_event.count() == 0:
            return 'Нет файлов'
        else:
            return obj.trade_union_photo_event.count()

    trade_union_photo_count.short_description = 'Количество фото'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Чат"""
    list_display = 'name', 'user_count', 'room_count', 'is_active', 'created', 'updated',
    list_editable = 'is_active',
    list_filter = 'is_active',
    readonly_fields = 'user_count', 'room_count', 'created', 'updated',
    search_fields = 'name',
    search_help_text = 'Поиск по названию чата'
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created'
    ordering = 'name',
    list_per_page = 20

    def user_count(self, obj):
        if obj.message_content.count() == 0:
            return 'Нет сотрудников'
        else:
            return obj.message_content.values('user').distinct().count()

    user_count.short_description = 'Количество сотрудников'

    def room_count(self, obj):
        if obj.message_content.count() == 0:
            return 'Нет сообщений'
        else:
            return obj.message_content.count()

    room_count.short_description = 'Количество сообщений'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Сообщение"""
    list_display = 'user', 'room', 'short_content', 'created', 'updated',
    list_filter = 'room__name',
    readonly_fields = 'user', 'created', 'updated',
    search_fields = 'user__fio', 'content',
    search_help_text = 'Поиск по названию чата и сотруднику'
    date_hierarchy = 'created'
    ordering = 'room',
    list_per_page = 20

    def short_content(self, obj):
        len_str = 200
        if obj.content:
            return obj.content[:len_str] + "..." if len(obj.content) > len_str else obj.content
        return "Информация не заполнена"

    short_content.short_description = 'Сообщение'

    def save_model(self, request, obj, form, change):
        # Автоматически назначать текущего пользователя, если он не указан.
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)
