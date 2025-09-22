import os
import dj_database_url
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Отключено для продакшена

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-b4d2a.up.railway.app',
    'https://*.up.railway.app',
]

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://bogdan:@localhost:5432/wagtail_portfolio',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Add WhiteNoise middleware for serving static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Configure WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Override STORAGES for WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# WhiteNoise settings
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# Wagtail settings
WAGTAIL_SITE_NAME = "Portfolio Site"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000')
WAGTAILADMIN_BASE_URL = BASE_URL

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'gunicorn.error': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}