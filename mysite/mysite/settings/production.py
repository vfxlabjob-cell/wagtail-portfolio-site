from .base import *
import os
import secrets

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
# Генерируем новый секретный ключ для продакшена
SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_urlsafe(50))

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

# CSRF настройки для Vercel
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.vercel.com',
]

# Включаем CSRF middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

# Настройки безопасности для продакшена
# Vercel обрабатывает SSL на уровне прокси
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Отключаем SSL redirect для Vercel - они сами это делают
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 31536000  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Настройки cookies для безопасности
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Настройки для статических файлов
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Настройки медиа файлов
# Используем S3/R2 storage только если все переменные настроены
if all([
    os.environ.get('AWS_ACCESS_KEY_ID'),
    os.environ.get('AWS_SECRET_ACCESS_KEY'),
    os.environ.get('AWS_STORAGE_BUCKET_NAME'),
    os.environ.get('AWS_S3_ENDPOINT_URL')
]):
    # Для Django 4.2+ используем STORAGES
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }
    # Для совместимости со старыми версиями
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    # R2 Settings
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_QUERYSTRING_AUTH = False  # Don't add auth params to URLs
    AWS_S3_FILE_OVERWRITE = False  # Don't overwrite files with same name
как это сделать     
    # Добавляем заголовки для CORS
    AWS_S3_OBJECT_PARAMETERS.update({
        'CacheControl': 'max-age=86400',
        'ACL': 'public-read',
    })
    
    # Set MEDIA_URL to R2 URL
    # Если есть custom domain, используйте его
    if AWS_S3_CUSTOM_DOMAIN:
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    else:
        # Используем основной Railway домен для медиа
        MEDIA_URL = '/media/'

    print("Using S3/R2 storage for media files")
    print(f"R2 Endpoint: {AWS_S3_ENDPOINT_URL}")
    print(f"R2 Bucket: {AWS_STORAGE_BUCKET_NAME}")
    print(f"R2 Access Key: {AWS_ACCESS_KEY_ID[:10]}...")
    print("MEDIA_URL set to /media/ for Railway domain compatibility")
else:
    # Fallback к локальному хранилищу
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
    print("Using local storage for media files")

# Настройки базы данных для продакшена
# Используем DATABASE_URL от Railway
import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
    print("Using PostgreSQL database from DATABASE_URL")
else:
    # Fallback к SQLite для локального тестирования
    print("WARNING: No DATABASE_URL found, using SQLite")

# Настройки email для продакшена
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Единственная настройка логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'gunicorn.access': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'gunicorn.error': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Создаем папку для логов если её нет
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# Wagtail production settings
WAGTAILADMIN_BASE_URL = f"https://{RAILWAY_PUBLIC_DOMAIN}" if RAILWAY_PUBLIC_DOMAIN else "http://localhost:8000"

print(f"Production settings loaded:")
print(f"- DEBUG: {DEBUG}")
print(f"- ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"- DATABASE: {'PostgreSQL' if DATABASE_URL else 'SQLite'}")
print(f"- WAGTAILADMIN_BASE_URL: {WAGTAILADMIN_BASE_URL}")
