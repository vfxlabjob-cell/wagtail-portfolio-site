"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.production")

application = get_wsgi_application()

# Use WhiteNoise to serve static files in production
try:
    from whitenoise import WhiteNoise
    from django.conf import settings
    application = WhiteNoise(application, root=settings.STATIC_ROOT)
except ImportError:
    # Fallback if WhiteNoise is not available
    pass
