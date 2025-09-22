#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.dev')
django.setup()

from django.contrib.auth.models import User

# Create superuser
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if User.objects.filter(username=username).exists():
    print(f'User {username} already exists')
else:
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created successfully')
