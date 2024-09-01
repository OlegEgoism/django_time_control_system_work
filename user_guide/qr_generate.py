# import qrcode
#
# data = "Пустовалов Олег"
# print('Данные QRCode -->', data)
#
# qr = qrcode.QRCode(
#     version=2,
#     box_size=30,
#     border=5,
#     error_correction=qrcode.constants.ERROR_CORRECT_Q,
# )
# qr.add_data(data)
# qr.make(fit=True)
# img = qr.make_image(fill_color="black", back_color="white")
# img.save(f"media/photo_qr/{data}.png")


import os
import qrcode
import transliterate  # Нужно установить пакет transliterate

data = "Пустовалов Олег Юрьевич"
print('Данные QRCode -->', data)

filename = transliterate.translit(data, reversed=True)
filename = filename.replace(" ", "_")  # Замена пробелов на символы подчеркивания
output_dir = "photo_qr"
os.makedirs(output_dir, exist_ok=True)

qr = qrcode.QRCode(  # Создание QR-кода
    version=2,
    box_size=30,
    border=5,
    error_correction=qrcode.constants.ERROR_CORRECT_Q,
)
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save(os.path.join(output_dir, f"{filename}.png"))  # Сохранение QR-кода
