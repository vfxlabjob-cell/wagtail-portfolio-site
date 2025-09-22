from .dev import *

# PostgreSQL Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wagtail_portfolio',
        'USER': 'bogdan',  # ваш пользователь PostgreSQL
        'PASSWORD': '',  # пароль если есть
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
