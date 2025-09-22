#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.dev')
django.setup()

from django.contrib.auth.models import User

# Update superuser password
username = 'admin'
password = 'admin123'

try:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f'Password updated for user {username}')
except User.DoesNotExist:
    print(f'User {username} does not exist')
