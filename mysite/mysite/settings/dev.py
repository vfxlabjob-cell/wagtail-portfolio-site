from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-tr+2ma$c^suczmnf*xv=!c6be9^vrrnjqgwk6khdy&f84o&!hl"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# CSRF settings for Railway
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-c60254.up.railway.app',
    'https://*.up.railway.app',
    'https://*.railway.app',
]

# Additional CSRF settings
CSRF_COOKIE_SECURE = False  # Set to False for Railway
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
