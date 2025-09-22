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

# Создаем новую главную страницу PortfolioIndexPage
home_page = PortfolioIndexPage(
    title="Portfolio",
    slug="portfolio", 
    intro="<p>Добро пожаловать в портфолио!</p>",
    show_in_menus=True
)

# Добавляем как дочернюю к корневой странице
root_page.add_child(instance=home_page)

# Публикуем страницу
home_page.save_revision().publish()

print(f'Создана новая главная страница: {home_page.title} (slug: {home_page.slug})')

# Перемещаем все страницы проектов к новой главной странице
old_home = Page.objects.get(id=10)  # "Welcome To"
children = old_home.get_children()

for child in children:
    child.move(home_page, pos='last-child')
    print(f'Перемещена страница: {child.title}')

print('\nСтруктура страниц:')
for page in Page.objects.all().order_by('depth', 'path'):
    indent = "  " * (page.depth - 1)
    print(f'{indent}- {page.title} (ID: {page.id}, Type: {page.__class__.__name__}, Live: {page.live})')
