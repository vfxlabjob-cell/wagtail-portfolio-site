from .base import *
import os

# Настройки для разработки с R2
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Cloudflare R2 Storage для разработки
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
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

# Настройки базы данных (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'wagtail_site'),
        'USER': os.environ.get('DB_USER', os.environ.get('USER', 'bogdan')),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Email backend для разработки
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
