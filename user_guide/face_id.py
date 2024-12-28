import os
import django
import time
from conf.settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
django.setup()

import cv2
import face_recognition
from django.utils import timezone
from user_guide.models import CustomUser, StatusLocation

time_update_camera = 30  # Через какое время обновляем дату
frame_count = 0
process_every_n_frame = 4  # Процессировать каждую рамку
image_folder = os.path.join(BASE_DIR, 'media/photo_user')  # Путь к папке с изображениями
known_face_encodings, known_face_names = [], []
camera_id = '01JC94TY3M363XG3V3TNDEZ4Y6'  # ID камеры
video_capture = cv2.VideoCapture(0)  # Захват видео с веб-камеры
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
last_record_times = {}  # Словарь для отслеживания времени последней записи для каждого сотрудника

# Загрузка известных лиц из базы данных
for filename in os.listdir(image_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_folder, filename)
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)
        if face_encoding:  # Если кодировка найдена
            known_face_encodings.append(face_encoding[0])  # Добавляем первую найденную кодировку
            known_face_names.append(filename)  # Сохраняем имя файла (которое будет связано с сотрудника)

# Основной цикл обработки видео
while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Не удалось захватить кадр.")
        break
    frame_count += 1
    if frame_count % process_every_n_frame == 0:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        if not face_locations:
            print("Лица не найдены в текущем кадре.")
        else:
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                slug = "Неизвестное лицо"
                if True in matches:
                    first_match_index = matches.index(True)
                    filename = known_face_names[first_match_index]
                    try:
                        custom_user = CustomUser.objects.get(photo=f'photo_user/{filename}')
                        if not custom_user.is_active:
                            print(f"Сотрудник {custom_user.username} не активен")
                            continue
                        slug = custom_user.slug.split('-')[0]  # Получаем поле slug сотрудника
                        current_time = time.time()
                        if custom_user.id_custom_user in last_record_times:
                            if current_time - last_record_times[custom_user.id_custom_user] >= time_update_camera:  # Через какое время обновляем дату
                                StatusLocation.objects.create(
                                    custom_user=custom_user,
                                    camera_id=camera_id,  # Указываем ID камеры
                                    created=timezone.now()  # Записываем текущее время
                                )
                                last_record_times[custom_user.id_custom_user] = current_time  # Обновляем время последней записи
                                print(f"Записан сотрудник: {custom_user.fio or custom_user.username}")
                        else:
                            StatusLocation.objects.create(
                                custom_user=custom_user,
                                camera_id=camera_id,
                                created=timezone.now()
                            )
                            last_record_times[custom_user.id_custom_user] = current_time  # Сохраняем время первой записи
                            print(f"Сотрудник: {custom_user.fio or custom_user.username}")
                    except CustomUser.DoesNotExist:
                        print(f"Сотрудник с фото {filename} не найден.")
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, slug.capitalize(), (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Выход по нажатию 'q'
        break

# Освобождение ресурсов
video_capture.release()
cv2.destroyAllWindows()
