from django import forms
from django.utils.timezone import make_aware

from .all_validator import phone_mobile_validator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Organizer, Camera, Address
from django.forms.widgets import DateTimeInput


class CustomUserCreationForm(UserCreationForm):
    """Пользовательская форма создания сотрудника"""

    class Meta:
        model = CustomUser
        fields = 'username', 'email', 'fio', 'slug', 'password1', 'password2'


class CustomUserChangeForm(UserChangeForm):
    """Пользовательская форма смены сотрудника"""

    class Meta:
        model = CustomUser
        fields = 'username', 'email', 'fio', 'slug'


class CustomUserForm(forms.ModelForm):
    """Редактирование данных сотрудника"""
    email = forms.EmailField(label='Почта: ', required=False, widget=forms.EmailInput(attrs={'class': 'form-control col-sm-3'}))
    phone_mobile = forms.CharField(label='Телефон мобильный: ', required=False, validators=[phone_mobile_validator], widget=forms.TextInput(attrs={'class': 'form-control col-sm-3', 'placeholder': '+375(__)___-__-__'}))
    phone_working = forms.CharField(label='Телефон рабочий: ', required=False, widget=forms.TextInput(attrs={'class': 'form-control col-sm-3', 'placeholder': '8(___)___-__-__'}))
    biography = forms.CharField(label='Биография: ', required=False, widget=forms.Textarea(attrs={'class': 'form-control col-sm-10', 'placeholder': 'Расскажите о себе', 'style': 'width: 800px; height: 600px;'}))

    class Meta:
        model = CustomUser
        fields = 'email', 'phone_mobile', 'phone_working', 'biography'


class StatusLocationFilterForm(forms.Form):
    """Отображение детальной информации"""
    FINDING_CHOICES_WITH_ALL = (('', 'Все'),) + Camera.FINDING_CHOICES  # Возможность выбрать все камеры
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Дата с")
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Дата по")
    finding = forms.ChoiceField(choices=FINDING_CHOICES_WITH_ALL, required=False, label="Нахождение")
    address = forms.ModelChoiceField(queryset=Address.objects.all(), required=False, label="Адрес камеры")


class OrganizerForm(forms.ModelForm):
    """Календарь органайзер"""

    class Meta:
        model = Organizer
        fields = ['title', 'description', 'start_time', 'end_time', 'custom_user']
        widgets = {
            'start_time': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['start_time'].initial = self.instance.start_time.strftime('%Y-%m-%dT%H:%M')
            self.fields['end_time'].initial = self.instance.end_time.strftime('%Y-%m-%dT%H:%M')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.start_time and not instance.start_time.tzinfo:
            instance.start_time = make_aware(instance.start_time)
        if instance.end_time and not instance.end_time.tzinfo:
            instance.end_time = make_aware(instance.end_time)
        if commit:
            instance.save()
        return instance