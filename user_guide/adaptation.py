import random

def generate_random_color():
    """Генерация случайного цвета в формате HEX"""
    return f"#{random.randint(0, 0xFFFFFF):06x}"