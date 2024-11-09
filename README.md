Команды для работы проекта

Запуск проекта
- Создает виртуальное окружение: .venv
- Загрузка библиотек в проект: pip install -r requirements.txt
- Подготовка миграций : python manage.py makemigrations
- Создание миграций в БД: python manage.py migrate
- Создание пользователя для админки: python manage.py createsuperuser
- Запуск сервера: python manage.py runserver
- Для заполнения базовых данных в БД: python manage.py loaddata db.json
- Создайте файл и установите зависимости для приложения в файл: .env

Redis
- Выполняем установку Redis в Docker. После выполняем загрузку образа Redis: docker pull redis
- Запускаем контейнер: docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
- Проверим, что наш контейнер запустился: docker ps
- Поднять на 8001:8001 порту: docker run -p 8001:8001 redis/redis-stack:latest
- Остановка сервиса редис: sudo docker stop *CONTAINER ID*
- Запуск редиса: sudo docker start *CONTAINER ID*
- Очистка порта (*port* по стандарту: 6379) если он занят: sudo lsof -i :*port* 
- Удалить порт который занят: sudo kill <PID>
- Остановка сервиса редис: sudo service redis-server stop
- Удаляем все остановленные контейнеры: sudo docker system prune -a
- Очистка всех ключей из Redis: flushall
- Открытие Redis в браузереж: http://localhost:8001/redis-stack/browser
- Поднять на 8001:8001 порту: docker run -p 8001:8001 redis/redis-stack:latest

[Запись экрана от 09.11.2024 22:09:09.webm](..%2F..%2F%D0%92%D0%B8%D0%B4%D0%B5%D0%BE%2F%D0%97%D0%B0%D0%BF%D0%B8%D1%81%D0%B8%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%2F%D0%97%D0%B0%D0%BF%D0%B8%D1%81%D1%8C%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BE%D1%82%2009.11.2024%2022%3A09%3A09.webm)