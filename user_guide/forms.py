from django import forms
from .all_validator import phone_mobile_validator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Camera, Address


class CustomUserCreationForm(UserCreationForm):
    """Пользовательская форма создания пользователя"""

    class Meta:
        model = CustomUser
        fields = 'username', 'email', 'fio', 'slug', 'password1', 'password2'


class CustomUserChangeForm(UserChangeForm):
    """Пользовательская форма смены пользователя"""

    class Meta:
        model = CustomUser
        fields = 'username', 'email', 'fio', 'slug'


class CustomUserForm(forms.ModelForm):
    """Редактирование данных пользователя"""
    photo = forms.ImageField(label='Фотография', required=False)
    phone_mobile = forms.CharField(label='Телефон мобильный', required=False, validators=[phone_mobile_validator], widget=forms.TextInput(attrs={'class': 'form-control col-sm-3', 'placeholder': '+375(00)000-00-00'}))
    biography = forms.CharField(label='Биография', required=False, widget=forms.Textarea(attrs={'class': 'form-control col-sm-12', 'placeholder': 'Раскажите о себе'}))

    class Meta:
        model = CustomUser
        fields = 'photo', 'phone_mobile', 'biography',


class StatusLocationFilterForm(forms.Form):
    """Отображение детальной информации"""
    FINDING_CHOICES_WITH_ALL = (('', 'Все'),) + Camera.FINDING_CHOICES  # Возможность выбрать все камеры
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Дата с")
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Дата по")
    finding = forms.ChoiceField(choices=FINDING_CHOICES_WITH_ALL, required=False, label="Нахождение")
    address = forms.ModelChoiceField(queryset=Address.objects.all(), required=False, label="Адрес камеры")
