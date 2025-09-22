#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.production')
django.setup()

from wagtail.models import Site
from django.contrib.auth.models import User

print("=== Настройка для Railway ===")

# Настраиваем Site для Railway
try:
    site = Site.objects.first()
    if site:
        site.hostname = 'web-production-c60254.up.railway.app'
        site.port = 443
        site.is_default_site = True
        site.save()
        print(f"✓ Site настроен: {site.hostname}:{site.port}")
    else:
        # Создаем новый site
        from wagtail.models import Page
        root_page = Page.objects.get(id=1)
        site = Site.objects.create(
            hostname='web-production-c60254.up.railway.app',
            port=443,
            root_page=root_page,
            is_default_site=True
        )
        print(f"✓ Site создан: {site.hostname}:{site.port}")
except Exception as e:
    print(f"✗ Ошибка настройки Site: {e}")

# Проверяем/создаем суперпользователя
try:
    admin_user = User.objects.filter(username='admin').first()
    if admin_user:
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.is_active = True
        admin_user.set_password('admin123')
        admin_user.save()
        print("✓ Пользователь admin обновлен")
    else:
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✓ Создан новый суперпользователь admin")
except Exception as e:
    print(f"✗ Ошибка настройки пользователя: {e}")

print("=== Настройка завершена ===")
