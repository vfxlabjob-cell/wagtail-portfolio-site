#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.dev')
django.setup()

from wagtail.models import Page
from home.models import PortfolioIndexPage

# Получаем корневую страницу
root_page = Page.objects.get(id=1)

# Проверяем, есть ли уже главная страница
existing_home = PortfolioIndexPage.objects.filter(depth=2).first()

if existing_home:
    print(f'Главная страница уже существует: {existing_home.title}')
else:
    # Создаем главную страницу
    home_page = PortfolioIndexPage(
        title="Home",
        slug="home",
        intro="<p>Добро пожаловать в портфолио!</p>",
        show_in_menus=True
    )
    
    # Добавляем как дочернюю к корневой странице
    root_page.add_child(instance=home_page)
    
    print(f'Создана главная страница: {home_page.title}')
    
    # Публикуем страницу
    home_page.save_revision().publish()
    print('Главная страница опубликована')

print('Структура страниц:')
for page in Page.objects.all().order_by('depth', 'path'):
    indent = "  " * (page.depth - 1)
    print(f'{indent}- {page.title} (ID: {page.id}, Type: {page.__class__.__name__}, Live: {page.live})')
