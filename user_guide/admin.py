from admin_auto_filters.filters import AutocompleteFilter

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from user_guide.models import (
    StatusLocation,
    Address,
    Subdivision,
    Position,
    CustomUser,
    Note,
    Camera,
    Setting
)


class AddressFilter(AutocompleteFilter):
    title = 'Адрес рабочего места'
    field_name = 'address'


class SubdivisionFilter(AutocompleteFilter):
    title = 'Подразделение'
    field_name = 'subdivision'


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
    #
    # def has_add_permission(self, request, obj=None):
    #     """Запретить добавление новых объектов"""
    #     return False


# ______________________________________________________
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Адрес рабочего места"""
    list_display = 'name', 'created', 'updated',
    readonly_fields = 'created', 'updated',
    search_fields = 'name',
    search_help_text = 'Поиск по адресу'
    list_per_page = 20


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Должность"""
    list_display = 'name', 'created', 'updated', 'count_position',
    readonly_fields = 'created', 'updated',
    search_fields = 'name',
    search_help_text = 'Поиск по должности'
    list_per_page = 20

    def count_position(self, obj):
        return obj.custom_user_position.count()

    count_position.short_description = 'Количество сотрудников'


@admin.register(Subdivision)
class SubdivisionAdmin(admin.ModelAdmin):
    """Подразделение"""
    list_display = 'name', 'created', 'updated', 'count_subdivision',
    readonly_fields = 'created', 'updated',
    search_fields = 'name',
    search_help_text = 'Поиск по подразделению'
    list_per_page = 20

    def count_subdivision(self, obj):
        return obj.custom_user_subdivision.count()

    count_subdivision.short_description = 'Количество сотрудников'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Заметка"""
    list_display = 'name', 'count_note',
    readonly_fields = 'created', 'updated',
    search_fields = 'name',
    search_help_text = 'Поиск по заметкам'
    list_per_page = 20

    def count_note(self, obj):
        return obj.custom_user_note.count()

    count_note.short_description = 'Количество сотрудников'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Сотрудник"""
    fieldsets = (
        (None, {
            'fields': ('username', 'password',)}),
        ('РАЗРЕШЕНИЯ', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined',)}),
        ('ЛИЧНЫЕ ДАННЫЕ', {
            'fields': ('preview_photo', 'photo', 'fio', 'birthday', 'biography', 'email', 'phone_mobile', 'phone_working', 'address', 'note', 'position', 'subdivision',)},),
    )
    list_display = 'username', 'preview_photo', 'fio', 'phone_mobile', 'phone_working', 'note', 'subdivision', 'position', 'is_active',
    list_filter = 'is_active', NoteFilter, SubdivisionFilter, PositionFilter,
    readonly_fields = 'last_login', 'date_joined', 'preview_photo',
    search_fields = 'username', 'fio', 'phone_mobile', 'phone_working', 'position', 'subdivision',
    search_help_text = 'Поиск по логину, имени пользователя и номеру телефона, должности, подразделению'
    inlines = StatusLocationInline,
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
    list_filter = CustomUserFilter, CameraFilter,
    readonly_fields = 'created',
    date_hierarchy = 'created'
    search_fields = 'custom_user__fio', 'camera__address__name'
    search_help_text = 'Поиск по ФИО и адресу местонажождения камеры'
    list_per_page = 20


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    """Камера"""
    fields = 'finding', 'address', 'is_active',
    list_display = '__str__', 'id_camera', 'is_active',
    list_filter = 'is_active', 'finding', AddressFilter,
    search_fields = 'address__name',
    search_help_text = 'Поиск по адресу местонажождения камеры'
    list_per_page = 20


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """Настройки"""
    fields = 'preview_logo', 'logo', 'name',
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
