import re
from django.core.exceptions import ValidationError


def phone_mobile_validator(phone_number):
    regular = r'^\+375\((?:25|29|33|44)\)\d{3}-\d{2}-\d{2}$'
    if re.fullmatch(regular, phone_number):
        return phone_number
    else:
        raise ValidationError('Некорректный формат номера телефона (формат +375(00)000-00-00)')
