#!/bin/bash

# Переходим в папку с Django проектом
cd mysite

# Выполняем миграции
python manage.py migrate

# Собираем статические файлы
python manage.py collectstatic --noinput

# Запускаем сервер
python manage.py runserver 0.0.0.0:$PORT --settings=mysite.settings.production
