#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.dev')
django.setup()

from django.contrib.auth.models import User

# Проверяем существующего пользователя
admin_user = User.objects.filter(username='admin').first()

if admin_user:
    print(f'Пользователь admin существует')
    print(f'Is superuser: {admin_user.is_superuser}')
    print(f'Is staff: {admin_user.is_staff}')
    print(f'Is active: {admin_user.is_active}')
    
    # Убеждаемся что он суперпользователь
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.is_active = True
    admin_user.set_password('admin123')
    admin_user.save()
    print('Пользователь admin обновлен')
else:
    # Создаем нового пользователя
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Создан новый суперпользователь admin')

print('Готово!')
