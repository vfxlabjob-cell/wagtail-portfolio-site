#!/usr/bin/env python
"""
Скрипт для очистки поврежденных сессий
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.no_csrf')
django.setup()

from django.contrib.sessions.models import Session
from django.utils import timezone

def clear_corrupted_sessions():
    """Очищает все сессии из базы данных"""
    try:
        # Удаляем все сессии
        deleted_count = Session.objects.all().delete()[0]
        print(f"Удалено {deleted_count} сессий")
        
        # Очищаем устаревшие сессии
        expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
        expired_count = expired_sessions.delete()[0]
        print(f"Удалено {expired_count} устаревших сессий")
        
        print("Сессии успешно очищены!")
        
    except Exception as e:
        print(f"Ошибка при очистке сессий: {e}")

if __name__ == "__main__":
    clear_corrupted_sessions()
