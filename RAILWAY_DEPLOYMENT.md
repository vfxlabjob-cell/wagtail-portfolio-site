# Railway Deployment Guide

## Проблемы и решения

### Проблема: Сайт деплоится успешно, но нет админ панели и страниц

**Причины:**
1. Не создается суперпользователь
2. Не создаются базовые страницы Wagtail
3. Проблемы со статическими файлами
4. Неправильные настройки базы данных

## Решение

### 1. Настройка переменных окружения в Railway

Добавьте следующие переменные в настройках вашего проекта Railway:

```
SECRET_KEY=your-very-long-and-secure-secret-key-here
ADMIN_PASSWORD=your-secure-admin-password
RAILWAY_PUBLIC_DOMAIN=https://your-app-name.up.railway.app
```

### 2. Автоматическая инициализация

Теперь при деплое автоматически выполняется:

1. **Миграции базы данных** - `python manage.py migrate`
2. **Сбор статических файлов** - `python manage.py collectstatic`
3. **Инициализация сайта** - `python manage.py setup_site`
   - Создание суперпользователя (admin)
   - Создание корневой страницы
   - Создание страницы Portfolio
   - Создание страницы Information
   - Настройка сайта Wagtail

### 3. Доступ к админ панели

После успешного деплоя:

- **Админ панель**: `https://your-app-name.up.railway.app/admin/`
- **Портфолио**: `https://your-app-name.up.railway.app/portfolio/`
- **Информация**: `https://your-app-name.up.railway.app/info/`

**Логин**: `admin`  
**Пароль**: значение переменной `ADMIN_PASSWORD`

### 4. Структура сайта

После инициализации у вас будет:

```
Root Page
├── Portfolio (главная страница)
│   └── [ваши проекты будут здесь]
└── Information
    └── [информационные страницы]
```

### 5. Проверка деплоя

1. Проверьте логи Railway на наличие ошибок
2. Убедитесь, что все переменные окружения установлены
3. Проверьте доступность `/admin/` и `/portfolio/`

### 6. Если что-то не работает

1. Проверьте логи в Railway Dashboard
2. Убедитесь, что все переменные окружения установлены
3. Попробуйте пересоздать проект Railway

## Команды для локального тестирования

```bash
# Переключиться на production настройки
export DJANGO_SETTINGS_MODULE=mysite.settings.production

# Выполнить миграции
python manage.py migrate --settings=mysite.settings.production

# Собрать статические файлы
python manage.py collectstatic --noinput --settings=mysite.settings.production

# Инициализировать сайт
python manage.py setup_site --settings=mysite.settings.production

# Запустить сервер
python manage.py runserver --settings=mysite.settings.production
```

## Важные файлы

- `Procfile` - команды запуска для Railway
- `railway.toml` - конфигурация Railway
- `mysite/home/management/commands/setup_site.py` - команда инициализации
- `mysite/mysite/settings/production.py` - production настройки