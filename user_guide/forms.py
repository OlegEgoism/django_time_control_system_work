from django import forms
from django.utils.safestring import mark_safe

from .all_validator import phone_mobile_validator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Пользовательская форма создания пользователя"""

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'fio', 'slug', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    """Пользовательская форма смены пользователя"""

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'fio', 'slug')


class CustomUserForm(forms.ModelForm):
    """Редактирование данных пользователя"""
    phone_mobile = forms.CharField(label='Телефон мобильный', help_text='Формат +375(00)000-00-00)', validators=[phone_mobile_validator], required=False)
    photo = forms.ImageField(label='Фотография', required=False)

    class Meta:
        model = CustomUser
        fields = 'photo', 'phone_mobile', 'birthday', 'biography',
