import os
import django
import cv2
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
django.setup()

from user_guide.models import CustomUser, StatusLocation, Camera

last_scan_time = None  # Переменная для хранения времени последнего сканирования
id_camera = '01J7QTM5045M40SRZ446R8T862'
seconds = 3

def video_reader():
    """Запуск через терминал включение камеры и запись данных в StatusLocation"""
    global last_scan_time
    cam = cv2.VideoCapture(0)  # включаем камеру
    detector = cv2.QRCodeDetector()  # включаем QRCode detector

    while True:
        _, img = cam.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            current_time = timezone.now()
            if last_scan_time is None or (current_time - last_scan_time) >= timedelta(seconds=seconds):
                print("Обнаружен QRCode -->", data)  # выводим в терминал ссылку
                try:
                    user = CustomUser.objects.get(fio=data)   # Проверяем существование пользователя

                    try:
                        camera = Camera.objects.get(id_camera=id_camera)
                        StatusLocation.objects.create(
                            custom_user=user,
                            camera=camera,
                            created=current_time
                        )
                        print(f"Запись для пользователя {user.fio} добавлена.")
                        last_scan_time = current_time  # Обновляем время последнего сканирования
                    except Camera.DoesNotExist:
                        print(f"Камера с ID {id_camera} не найдена.")
                except CustomUser.DoesNotExist:
                    print("Пользователь не найден.")
            else:
                print("Слишком рано для повторного сканирования.")
        cv2.imshow("img", img)
        if cv2.waitKey(1) == ord("Q"):  # Время сканирования QRCode
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_reader()
