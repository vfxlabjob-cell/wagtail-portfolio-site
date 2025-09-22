# 🚀 Railway Deployment Guide

Быстрый и простой деплой на Railway без нервов!

## 📋 Шаги деплоя

### 1. Подготовка репозитория
```bash
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

### 2. Создание проекта на Railway

1. **Зайдите на [Railway.app](https://railway.app)**
2. **Нажмите "New Project"**
3. **Выберите "Deploy from GitHub repo"**
4. **Выберите ваш репозиторий `wagtail_site`**
5. **Нажмите "Deploy Now"**

### 3. Настройка переменных окружения

В настройках проекта Railway добавьте:

```bash
SECRET_KEY=your-very-secret-key-here-make-it-long-and-random
DEBUG=False
DJANGO_SETTINGS_MODULE=mysite.settings.production
RAILWAY_PUBLIC_DOMAIN=https://your-app-name.railway.app
```

### 4. Добавление PostgreSQL базы данных

1. **В Railway проекте нажмите "+ New"**
2. **Выберите "Database" → "PostgreSQL"**
3. **Railway автоматически создаст `DATABASE_URL`**

### 5. Настройка домена (опционально)

1. **В настройках проекта найдите "Domains"**
2. **Добавьте ваш домен или используйте Railway домен**

## 🔧 Автоматические команды

Railway автоматически выполнит:
- `python manage.py migrate` - создание таблиц БД
- `python manage.py collectstatic --noinput` - сбор статических файлов
- `gunicorn mysite.wsgi:application` - запуск сервера

## 📁 Структура файлов для Railway

```
wagtail_site/
├── railway.toml          # Конфигурация Railway
├── Procfile              # Команды запуска
├── runtime.txt           # Версия Python
├── requirements.txt      # Зависимости
├── railway_env_example.txt # Пример переменных
└── mysite/
    └── mysite/
        └── settings/
            └── production.py # Production настройки
```

## 🎯 Что происходит при деплое

1. **Railway клонирует ваш репозиторий**
2. **Устанавливает зависимости из `requirements.txt`**
3. **Выполняет миграции базы данных**
4. **Собирает статические файлы**
5. **Запускает Gunicorn сервер**
6. **Ваш сайт доступен по Railway URL**

## 🚨 Возможные проблемы и решения

### Проблема: "No module named 'mysite.settings'"
**Решение:** Убедитесь, что `DJANGO_SETTINGS_MODULE=mysite.settings.production`

### Проблема: "Database connection failed"
**Решение:** Проверьте, что PostgreSQL база данных добавлена в проект

### Проблема: "Static files not found"
**Решение:** Убедитесь, что `collectstatic` выполняется в Procfile

### Проблема: "SECRET_KEY not set"
**Решение:** Добавьте `SECRET_KEY` в переменные окружения Railway

## 🎉 После успешного деплоя

1. **Ваш сайт будет доступен по Railway URL**
2. **Создайте суперпользователя:**
   ```bash
   railway run python manage.py createsuperuser
   ```
3. **Создайте контент сайта:**
   ```bash
   railway run python manage.py create_site_content
   ```

## 🔗 Полезные ссылки

- [Railway Documentation](https://docs.railway.app/)
- [Django on Railway](https://docs.railway.app/guides/django)
- [Railway CLI](https://docs.railway.app/develop/cli)

## 💡 Советы

- **Используйте Railway CLI** для удобного управления проектом
- **Настройте автоматические деплои** из main ветки
- **Используйте Railway переменные** для секретных данных
- **Мониторьте логи** в Railway dashboard

---

**Готово! Ваш сайт будет работать на Railway! 🚀**
