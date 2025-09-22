# Wagtail Portfolio Site

Современный портфолио сайт на Django + Wagtail CMS.

## 🚀 Особенности

- **Wagtail CMS** - мощная система управления контентом
- **Адаптивный дизайн** - работает на всех устройствах
- **Фильтрация проектов** по категориям
- **Управление медиа** - изображения и видео
- **Админ панель** для управления контентом

## 📋 Требования

- Python 3.12+
- Django 5.2+
- Wagtail 6.0+

## 🛠 Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <your-repo-url>
   cd wagtail_site
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте базу данных:**
   ```bash
   cd mysite
   python manage.py migrate
   ```

5. **Создайте суперпользователя:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Создайте контент сайта:**
   ```bash
   python manage.py create_site_content
   ```

7. **Запустите сервер:**
   ```bash
   python manage.py runserver
   ```

## 🌐 Доступ

- **Сайт:** http://127.0.0.1:8000/
- **Админка:** http://127.0.0.1:8000/admin/

## 📁 Структура проекта

```
wagtail_site/
├── mysite/                 # Django проект
│   ├── home/              # Главное приложение
│   ├── contacts/          # Контакты
│   ├── mysite/            # Настройки
│   └── manage.py          # Django команды
├── requirements.txt       # Зависимости
└── README.md             # Документация
```

## 🎨 Управление контентом

### Создание проектов
1. Зайдите в админку
2. Перейдите в "Pages" → "Home"
3. Нажмите "Add child page" → "Project Page"
4. Заполните информацию о проекте

### Создание категорий
1. В админке перейдите в "Snippets" → "Project Categories"
2. Нажмите "Add Project Category"
3. Заполните название и описание

## 🚀 Деплой

### Vercel
1. Подключите репозиторий к Vercel
2. Настройте переменные окружения
3. Деплой автоматически запустится

### Railway
1. Подключите репозиторий к Railway
2. Настройте переменные окружения
3. Деплой автоматически запустится

### Heroku
1. Создайте приложение в Heroku
2. Подключите репозиторий
3. Настройте переменные окружения
4. Деплой через Git

## 🔧 Настройка

### Переменные окружения
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your-database-url
```

### Статические файлы
```bash
python manage.py collectstatic
```

## 📝 Лицензия

MIT License

## 🤝 Поддержка

Если у вас есть вопросы или проблемы, создайте issue в репозитории.