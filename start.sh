#!/bin/bash

# Переходим в папку с Django проектом
cd mysite

# Выполняем миграции
python manage.py migrate

# Собираем статические файлы
python manage.py collectstatic --noinput

# Запускаем Gunicorn сервер
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
