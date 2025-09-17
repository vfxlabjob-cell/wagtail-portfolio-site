# Wagtail Portfolio Site

Современный портфолио сайт на Wagtail CMS с интеграцией Cloudflare R2 для хранения медиафайлов.

## Особенности

- 🎨 Современный дизайн с темной темой
- 📱 Адаптивная верстка
- 🎬 Поддержка видео контента
- 🖼️ Оптимизированные изображения
- 🌍 CDN через Cloudflare R2
- 📄 Информационные страницы (About, Contact, Privacy Policy, Terms of Service)
- 🔍 Поиск по сайту
- 📊 Админ панель Wagtail

## Технологии

- **Backend**: Django + Wagtail CMS
- **Database**: PostgreSQL
- **Storage**: Cloudflare R2
- **Frontend**: HTML, CSS, JavaScript, GSAP
- **Deployment**: Railway

## Структура проекта

```
mysite/
├── home/                    # Основное приложение
│   ├── models.py           # Модели страниц
│   ├── templates/          # Шаблоны
│   └── wagtail_hooks.py    # Хуки Wagtail
├── contacts/               # Контактное приложение
├── search/                 # Поиск
├── mysite/
│   ├── settings/           # Настройки Django
│   └── static/            # Статические файлы
└── media/                 # Медиа файлы (локально)
```

## Установка и запуск

### Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd wagtail_site
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env файл
```

5. Выполните миграции:
```bash
python mysite/manage.py migrate
```

6. Создайте суперпользователя:
```bash
python mysite/manage.py createsuperuser
```

7. Запустите сервер:
```bash
python mysite/manage.py runserver
```

### Переменные окружения

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost

# Database
DB_NAME=wagtail_site
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Cloudflare R2
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
```

## Деплой на Railway

1. Подключите репозиторий к Railway
2. Настройте переменные окружения в Railway Dashboard
3. Railway автоматически выполнит деплой

## Структура страниц

- **Home** - Главная страница с портфолио
- **Cards** - Раздел с карточками проектов
- **Information Pages** - Информационные страницы
  - About Us
  - Contact Us
  - Privacy Policy
  - Terms of Service

## Администрирование

Доступ к админ панели: `/admin/`

## Лицензия

MIT License
