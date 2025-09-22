# Railway Deployment Guide

## Шаги для деплоя на Railway

### 1. Подготовка проекта
- Убедитесь что все файлы закоммичены в git
- Проект должен быть в корне репозитория

### 2. Создание проекта на Railway
1. Зайдите на https://railway.app
2. Нажмите "New Project"
3. Выберите "Deploy from GitHub repo"
4. Выберите ваш репозиторий `vfxlabjob-cell/wagtail-portfolio-site`

### 3. Настройка переменных окружения
В настройках проекта Railway добавьте следующие переменные:

```
SECRET_KEY=your-very-secret-key-here
DEBUG=False
DJANGO_SETTINGS_MODULE=mysite.settings.production
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123
```

### 4. Настройка базы данных
1. В Railway dashboard нажмите "New" → "Database" → "PostgreSQL"
2. Railway автоматически добавит переменную `DATABASE_URL`

### 5. Настройка домена
1. В настройках сервиса включите "Generate Domain"
2. Скопируйте полученный домен
3. Добавьте переменную `RAILWAY_PUBLIC_DOMAIN=https://your-app-name.railway.app`

### 6. Деплой
1. Railway автоматически запустит деплой при пуше в main ветку
2. Проверьте логи в Railway dashboard

### 7. Проверка
После успешного деплоя:
- Откройте ваш сайт по полученному домену
- Зайдите в админку: `https://your-domain.railway.app/admin/`
- Логин: `admin`, пароль: `admin123`

## Структура файлов для деплоя

```
/
├── Procfile                    # Команды запуска
├── railway.toml               # Конфигурация Railway
├── railway_env_example.txt    # Пример переменных окружения
├── requirements.txt           # Python зависимости
├── mysite/                    # Django проект
│   ├── manage.py
│   ├── mysite/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   └── production.py  # Настройки для продакшена
│   │   └── wsgi.py
│   └── ...
└── README.md
```

## Возможные проблемы

### Проблема: "Unexposed service"
**Решение:** Включите "Generate Domain" в настройках сервиса

### Проблема: Статические файлы не загружаются
**Решение:** Убедитесь что `whitenoise` добавлен в middleware и настроен правильно

### Проблема: Ошибки миграции
**Решение:** Проверьте что `DATABASE_URL` настроен правильно

### Проблема: Нет админки
**Решение:** Проверьте что команда `create_superuser` выполнилась успешно в логах
