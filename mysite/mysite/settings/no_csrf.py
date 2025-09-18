from .base import *
import os
import secrets

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Отключаем для продакшена

# Настройки для обработки ошибок
ALLOWED_HOSTS = ['*']  # Разрешаем все хосты
ADMINS = [('Admin', 'admin@example.com')]  # Для отправки ошибок

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_urlsafe(50))

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']  # Разрешаем все хосты

# CSRF настройки для Railway (даже если отключен)
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-c60254.up.railway.app',
    'https://web-production-c60254.up.railway.app/',
    'https://*.up.railway.app',
    'https://*.up.railway.app/',
]

# Полностью отключаем CSRF
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = None
CSRF_COOKIE_DOMAIN = None
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_AGE = 31449600
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_TOKEN_GET_PARAM = 'csrfmiddlewaretoken'
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'

# Дополнительные настройки для полного отключения CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-c60254.up.railway.app',
    'https://web-production-c60254.up.railway.app/',
    'https://*.up.railway.app',
    'https://*.up.railway.app/',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Отключаем CSRF для всех представлений
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_DOMAIN = None
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'

# Дополнительные настройки для отключения CSRF
CSRF_COOKIE_AGE = None
CSRF_COOKIE_DOMAIN = None
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_SAMESITE = None
CSRF_COOKIE_SECURE = False
CSRF_USE_SESSIONS = False

# MIDDLEWARE БЕЗ CSRF
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Для статических файлов
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # CSRF MIDDLEWARE ПОЛНОСТЬЮ УБРАН
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

# Настройки безопасности (отключены)
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Настройки cookies (отключены)
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1209600  # 2 недели
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Настройки сессий для исправления "Session data corrupted"
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'wagtail_sessionid'
SESSION_COOKIE_SAMESITE = 'Lax'

# Настройки базы данных
import dj_database_url
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost:5432/wagtail_site')
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

# Настройки для статических файлов
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Настройки для поиска статических файлов
# STATICFILES_DIRS = []  # Убираем несуществующую директорию

# Настройки для статических файлов в продакшене
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Настройки медиа файлов
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Локальное хранилище (fallback)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# R2/Cloudflare Settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_FILE_OVERWRITE = False
AWS_S3_VERIFY = False  # Для R2
AWS_S3_REGION_NAME = 'auto'  # Для Cloudflare R2

# Если R2 настроен, используем его, иначе локальное хранилище
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/' if AWS_S3_CUSTOM_DOMAIN else f'https://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL.replace("https://", "")}/'
else:
    # Fallback на локальное хранилище
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Логирование - минимизируем для Railway
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',  # Только предупреждения и ошибки
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',  # Только предупреждения и ошибки
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',  # Только ошибки БД
            'propagate': False,
        },
        'django.template': {
            'handlers': ['console'],
            'level': 'ERROR',  # Только ошибки шаблонов
            'propagate': False,
        },
    },
}
