# import os
# import cv2
# import face_recognition
#
# from conf.settings import BASE_DIR
#
# frame_count = 0
# process_every_n_frame = 3  # Процессировать каждую 3-ю рамку
# image_folder = os.path.join(BASE_DIR, 'media/photo_user')  # Путь к папке с изображениями
# known_face_encodings, known_face_names = [], []
# video_capture = cv2.VideoCapture(0)  # Захват видео с веб-камеры
# video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#
# for filename in os.listdir(image_folder):
#     if filename.endswith(('.png', '.jpg', '.jpeg')):
#         image_path = os.path.join(image_folder, filename)
#         image = face_recognition.load_image_file(image_path)
#         face_encoding = face_recognition.face_encodings(image)
#         if face_encoding:  # Если кодировка найдена
#             known_face_encodings.append(face_encoding[0])  # Добавляем первую найденную кодировку
#             known_face_names.append(filename)  # Сохраняем имя файла
# while True:
#     ret, frame = video_capture.read()  # Чтение кадра из видео
#     if not ret:
#         print("Не удалось захватить кадр.")
#         break
#     frame_count += 1
#     if frame_count % process_every_n_frame == 0:
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Преобразуем BGR (OpenCV) в RGB
#         face_locations = face_recognition.face_locations(rgb_frame, model="hog")  # Используем модель "hog" для быстрого распознавания лиц
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#         if not face_locations:  # Проверяем, найдены ли лица
#             print("Лица не найдены в текущем кадре.")
#         else:
#             for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#                 matches = face_recognition.compare_faces(known_face_encodings, face_encoding)  # Сравниваем лица с известными кодировками
#                 name = "Неизвестное лицо"
#                 if True in matches:  # Если есть совпадение, берем имя
#                     first_match_index = matches.index(True)
#                     name = known_face_names[first_match_index]
#                     print(name)
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#                 cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#     cv2.imshow('Video', frame)  # Показываем кадр с распознанными лицами
#     if cv2.waitKey(1) & 0xFF == ord('q'):  # Выходим из цикла, если нажата клавиша 'q'
#         break
#
# video_capture.release()
# cv2.destroyAllWindows()


# import os
# import cv2
# import face_recognition
# from conf.settings import BASE_DIR
# from django.utils import timezone
# from user_guide.models import CustomUser, StatusLocation
#
# # Конфигурация
# frame_count = 0
# process_every_n_frame = 3  # Процессировать каждую 3-ю рамку
# image_folder = os.path.join(BASE_DIR, 'media/photo_user')  # Путь к папке с изображениями
# known_face_encodings, known_face_names = [], []
# camera_id = '0191d2ca-9b37-e294-8bfc-0938553497c5'  # ID камеры
#
# # Захват видео с веб-камеры
# video_capture = cv2.VideoCapture(0)
# video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#
# # Загрузка известных лиц из базы данных
# for filename in os.listdir(image_folder):
#     if filename.endswith(('.png', '.jpg', '.jpeg')):
#         image_path = os.path.join(image_folder, filename)
#         image = face_recognition.load_image_file(image_path)
#         face_encoding = face_recognition.face_encodings(image)
#         if face_encoding:  # Если кодировка найдена
#             known_face_encodings.append(face_encoding[0])  # Добавляем первую найденную кодировку
#             known_face_names.append(filename)  # Сохраняем имя файла (которое будет связано с пользователем)
#
# # Основной цикл обработки видео
# while True:
#     ret, frame = video_capture.read()
#     if not ret:
#         print("Не удалось захватить кадр.")
#         break
#
#     frame_count += 1
#
#     # Обработка каждого N-го кадра
#     if frame_count % process_every_n_frame == 0:
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         face_locations = face_recognition.face_locations(rgb_frame, model="hog")
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#
#         if not face_locations:
#             print("Лица не найдены в текущем кадре.")
#         else:
#             for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#                 matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#                 name = "Неизвестное лицо"
#
#                 # Проверяем, есть ли совпадения
#                 if True in matches:
#                     first_match_index = matches.index(True)
#                     filename = known_face_names[first_match_index]
#                     name = filename
#
#                     # Находим пользователя по фото (предполагается, что фото связано с пользователем)
#                     try:
#                         custom_user = CustomUser.objects.get(photo=f'photo_user/{filename}')
#
#                         # Записываем данные в модель StatusLocation
#                         StatusLocation.objects.create(
#                             custom_user=custom_user,
#                             camera_id=camera_id,  # Указываем ID камеры
#                             created=timezone.now()  # Записываем текущее время
#                         )
#
#                         print(f"Записан пользователь: {custom_user.fio or custom_user.username}")
#
#                     except CustomUser.DoesNotExist:
#                         print(f"Пользователь с фото {filename} не найден.")
#
#                 # Отображаем результат на экране
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#                 cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#
#     # Показываем видео
#     cv2.imshow('Video', frame)
#
#     # Выход по нажатию 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # Освобождение ресурсов
# video_capture.release()
# cv2.destroyAllWindows()


# import os
# from conf.settings import BASE_DIR
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
# import cv2
# import face_recognition
# from django.utils import timezone
# from user_guide.models import CustomUser, StatusLocation
#
# frame_count = 0
# process_every_n_frame = 3  # Процессировать каждую 3-ю рамку
# image_folder = os.path.join(BASE_DIR, 'media/photo_user')  # Путь к папке с изображениями
# known_face_encodings, known_face_names = [], []
# camera_id = '0191d2ca-9b37-e294-8bfc-0938553497c5'  # ID камеры
# video_capture = cv2.VideoCapture(0)
# video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#
# # Загрузка известных лиц из базы данных
# for filename in os.listdir(image_folder):
#     if filename.endswith(('.png', '.jpg', '.jpeg')):
#         image_path = os.path.join(image_folder, filename)
#         image = face_recognition.load_image_file(image_path)
#         face_encoding = face_recognition.face_encodings(image)
#         if face_encoding:  # Если кодировка найдена
#             known_face_encodings.append(face_encoding[0])  # Добавляем первую найденную кодировку
#             known_face_names.append(filename)  # Сохраняем имя файла (которое будет связано с пользователем)
#
# # Основной цикл обработки видео
# while True:
#     ret, frame = video_capture.read()
#     if not ret:
#         print("Не удалось захватить кадр.")
#         break
#
#     frame_count += 1
#
#     # Обработка каждого N-го кадра
#     if frame_count % process_every_n_frame == 0:
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         face_locations = face_recognition.face_locations(rgb_frame, model="hog")
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#
#         if not face_locations:
#             print("Лица не найдены в текущем кадре.")
#         else:
#             for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#                 matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#                 name = "Неизвестное лицо"
#
#                 # Проверяем, есть ли совпадения
#                 if True in matches:
#                     first_match_index = matches.index(True)
#                     filename = known_face_names[first_match_index]
#                     name = filename
#
#                     # Находим пользователя по фото (предполагается, что фото связано с пользователем)
#                     try:
#                         custom_user = CustomUser.objects.get(photo=f'photo_user/{filename}')
#
#                         # Записываем данные в модель StatusLocation
#                         StatusLocation.objects.create(
#                             custom_user=custom_user,
#                             camera_id=camera_id,  # Указываем ID камеры
#                             created=timezone.now()  # Записываем текущее время
#                         )
#
#                         print(f"Записан пользователь: {custom_user.fio or custom_user.username}")
#
#                     except CustomUser.DoesNotExist:
#                         print(f"Пользователь с фото {filename} не найден.")
#
#                 # Отображаем результат на экране
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#                 cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#
#     # Показываем видео
#     cv2.imshow('Video', frame)
#
#     # Выход по нажатию 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # Освобождение ресурсов
# video_capture.release()
# cv2.destroyAllWindows()


import os
import django
from conf.settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
django.setup()
import cv2
import face_recognition
from django.utils import timezone
from user_guide.models import CustomUser, StatusLocation

frame_count = 0
process_every_n_frame = 3  # Процессировать каждую 3-ю рамку
image_folder = os.path.join(BASE_DIR, 'media/photo_user')  # Путь к папке с изображениями
known_face_encodings, known_face_names = [], []
camera_id = '0191d2ca-9b37-e294-8bfc-0938553497c5'  # ID камеры

video_capture = cv2.VideoCapture(0)  # Захват видео с веб-камеры
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Загрузка известных лиц из базы данных
for filename in os.listdir(image_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_folder, filename)
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)
        if face_encoding:  # Если кодировка найдена
            known_face_encodings.append(face_encoding[0])  # Добавляем первую найденную кодировку
            known_face_names.append(filename)  # Сохраняем имя файла (которое будет связано с пользователем)

# Основной цикл обработки видео
while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Не удалось захватить кадр.")
        break

    frame_count += 1

    # Обработка каждого N-го кадра
    if frame_count % process_every_n_frame == 0:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if not face_locations:
            print("Лица не найдены в текущем кадре.")
        else:
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Неизвестное лицо"

                # Проверяем, есть ли совпадения
                if True in matches:
                    first_match_index = matches.index(True)
                    filename = known_face_names[first_match_index]
                    name = filename
                    # Находим пользователя по фото (предполагается, что фото связано с пользователем)
                    try:
                        custom_user = CustomUser.objects.get(photo=f'photo_user/{filename}')

                        # Записываем данные в модель StatusLocation
                        StatusLocation.objects.create(
                            custom_user=custom_user,
                            camera_id=camera_id,  # Указываем ID камеры
                            created=timezone.now()  # Записываем текущее время
                        )
                        print(f"Записан пользователь: {custom_user.fio or custom_user.username}")
                    except CustomUser.DoesNotExist:
                        print(f"Пользователь с фото {filename} не найден.")

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Выход по нажатию 'q'
        break

video_capture.release()
cv2.destroyAllWindows()
