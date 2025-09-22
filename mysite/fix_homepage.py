#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.dev')
django.setup()

from wagtail.models import Page
from home.models import PortfolioIndexPage

# Получаем существующую страницу "Welcome To"
welcome_page = Page.objects.get(id=10)

print(f'Найдена страница: {welcome_page.title} (тип: {welcome_page.__class__.__name__})')

# Создаем новую PortfolioIndexPage
home_page = PortfolioIndexPage(
    title="Home",
    slug="home",
    intro="<p>Добро пожаловать в портфолио!</p>",
    show_in_menus=True
)

# Получаем корневую страницу
root_page = Page.objects.get(id=1)

# Добавляем новую главную страницу
root_page.add_child(instance=home_page)

# Публикуем страницу
home_page.save_revision().publish()
print(f'Создана новая главная страница: {home_page.title}')

# Перемещаем все дочерние страницы от "Welcome To" к новой главной странице
children = welcome_page.get_children()
for child in children:
    child.move(home_page, pos='last-child')
    print(f'Перемещена страница: {child.title}')

print('Структура страниц после исправления:')
for page in Page.objects.all().order_by('depth', 'path'):
    indent = "  " * (page.depth - 1)
    print(f'{indent}- {page.title} (ID: {page.id}, Type: {page.__class__.__name__}, Live: {page.live})')
