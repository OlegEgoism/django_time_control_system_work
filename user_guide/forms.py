from django import forms
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
    class Meta:
        model = CustomUser
        fields = 'phone_mobile', 'birthday', 'biography',
