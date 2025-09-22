from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-tr+2ma$c^suczmnf*xv=!c6be9^vrrnjqgwk6khdy&f84o&!hl"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# PostgreSQL Database (по умолчанию)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wagtail_portfolio',
        'USER': 'bogdan',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

try:
    from .local import *
except ImportError:
    pass
