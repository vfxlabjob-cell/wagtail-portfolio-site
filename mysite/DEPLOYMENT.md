# Инструкция по деплою сайта

## 🚀 Варианты хостинга

### 1. Heroku (Рекомендуется для начинающих)
**Плюсы:** Простой деплой, автоматические обновления, встроенная база данных
**Минусы:** Платный после бесплатного периода

#### Шаги для деплоя на Heroku:
1. Установите Heroku CLI
2. Создайте аккаунт на heroku.com
3. Выполните команды:
```bash
heroku login
heroku create your-site-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
heroku config:set ALLOWED_HOSTS=your-site-name.herokuapp.com
git add .
git commit -m "Prepare for deployment"
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### 2. DigitalOcean App Platform
**Плюсы:** Хорошая производительность, разумные цены
**Минусы:** Требует больше настроек

### 3. Railway
**Плюсы:** Простой деплой, хорошая производительность
**Минусы:** Новый сервис

### 4. VPS (Virtual Private Server)
**Плюсы:** Полный контроль, дешевле для больших проектов
**Минусы:** Требует администрирования

## 🔧 Подготовка к деплою

### 1. Выберите базу данных:

#### **SQLite (простой вариант):**
- ✅ Уже настроена
- ❌ Максимум ~100 пользователей
- ❌ Нет масштабирования

#### **PostgreSQL (рекомендуется):**
- ✅ Поддержка тысяч пользователей
- ✅ Масштабирование
- ❌ Требует установки

**Установка PostgreSQL на macOS:**
```bash
brew install postgresql
brew services start postgresql
createdb wagtail_site
```

### 2. Установите зависимости для продакшена:
```bash
pip install -r requirements.txt
```

### 2. Соберите статические файлы:
```bash
python manage.py collectstatic --noinput
```

### 3. Выполните миграции:
```bash
python manage.py migrate
```

### 4. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

## 🔒 Настройки безопасности

### Переменные окружения (создайте .env файл):
```
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Settings
DB_NAME=wagtail_site
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Cloudflare R2 Settings
AWS_ACCESS_KEY_ID=your-api-token
AWS_SECRET_ACCESS_KEY=your-api-token
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
AWS_S3_CUSTOM_DOMAIN=your-bucket-name.your-domain.com
```

### Важные настройки безопасности:
- ✅ DEBUG = False
- ✅ SECRET_KEY - длинный случайный ключ
- ✅ ALLOWED_HOSTS - только ваши домены
- ✅ HTTPS редирект
- ✅ Безопасные cookies
- ✅ HSTS заголовки

## 📁 Структура файлов для деплоя

```
mysite/
├── Procfile                 # Конфигурация для Heroku
├── runtime.txt             # Версия Python
├── requirements.txt        # Зависимости
├── env_example.txt         # Пример переменных окружения
├── DEPLOYMENT.md          # Эта инструкция
├── mysite/
│   ├── settings/
│   │   ├── base.py        # Базовые настройки
│   │   ├── dev.py         # Настройки разработки
│   │   └── production.py  # Настройки продакшена
│   └── wsgi.py           # WSGI конфигурация
└── staticfiles/          # Собранные статические файлы
```

## 🚨 Проблемы и решения

### Проблема: Статические файлы не загружаются
**Решение:** Убедитесь, что выполнили `collectstatic` и настроили STATIC_ROOT

### Проблема: База данных не подключается
**Решение:** Проверьте переменные окружения DB_*

### Проблема: 500 ошибка
**Решение:** Проверьте логи: `heroku logs --tail`

### Проблема: Медиа файлы не загружаются
**Решение:** Настройте CDN или внешнее хранилище (AWS S3, Cloudinary)

## 📊 Мониторинг

### Логи:
```bash
heroku logs --tail
```

### Статистика:
```bash
heroku ps
heroku addons
```

## 🔄 Обновления

### Для обновления сайта:
```bash
git add .
git commit -m "Update site"
git push heroku main
heroku run python manage.py migrate
```

## 💰 Стоимость

### Heroku:
- Бесплатно: 550 часов в месяц
- Hobby: $7/месяц
- Professional: $25/месяц

### DigitalOcean:
- Basic: $5/месяц
- Professional: $12/месяц

### Railway:
- Hobby: $5/месяц
- Pro: $20/месяц

## 🎯 Рекомендации

1. **Начните с Heroku** - самый простой для начинающих
2. **Используйте PostgreSQL** - лучше SQLite для продакшена
3. **Настройте CDN** для медиа файлов
4. **Регулярно делайте бэкапы** базы данных
5. **Мониторьте логи** для выявления проблем
