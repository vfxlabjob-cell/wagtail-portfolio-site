#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.dev')
django.setup()

from wagtail.models import Page
from home.models import PortfolioIndexPage
from django.db import transaction

# Получаем существующую страницу "Welcome To"
welcome_page = Page.objects.get(id=10)

print(f'Найдена страница: {welcome_page.title} (тип: {welcome_page.__class__.__name__})')

# Создаем новую PortfolioIndexPage с теми же данными
with transaction.atomic():
    # Создаем новую PortfolioIndexPage
    new_home_page = PortfolioIndexPage(
        title=welcome_page.title,
        slug=welcome_page.slug,
        intro="<p>Добро пожаловать в портфолио!</p>",
        show_in_menus=welcome_page.show_in_menus,
        live=welcome_page.live,
        has_unpublished_changes=welcome_page.has_unpublished_changes,
        content_type=welcome_page.content_type,
        path=welcome_page.path,
        depth=welcome_page.depth,
        numchild=welcome_page.numchild,
        url_path=welcome_page.url_path,
        owner=welcome_page.owner,
        locked=welcome_page.locked,
        locked_by=welcome_page.locked_by,
        locked_at=welcome_page.locked_at,
        first_published_at=welcome_page.first_published_at,
        last_published_at=welcome_page.last_published_at,
        latest_revision_created_at=welcome_page.latest_revision_created_at,
        live_revision=welcome_page.live_revision,
        go_live_at=welcome_page.go_live_at,
        expire_at=welcome_page.expire_at,
        expired=welcome_page.expired,
        alias_of=welcome_page.alias_of,
        draft_title=welcome_page.draft_title,
        draft_slug=welcome_page.draft_slug,
        search_description=welcome_page.search_description,
        seo_title=welcome_page.seo_title,
        show_in_menus_default=welcome_page.show_in_menus_default,
        locale=welcome_page.locale,
        translation_key=welcome_page.translation_key,
    )
    
    # Сохраняем новую страницу
    new_home_page.save()
    
    # Получаем всех детей старой страницы
    children = welcome_page.get_children()
    for child in children:
        child.move(new_home_page, pos='last-child')
        print(f'Перемещена страница: {child.title}')
    
    # Удаляем старую страницу
    welcome_page.delete()
    
    print(f'Страница преобразована в PortfolioIndexPage: {new_home_page.title}')

print('Структура страниц после преобразования:')
for page in Page.objects.all().order_by('depth', 'path'):
    indent = "  " * (page.depth - 1)
    print(f'{indent}- {page.title} (ID: {page.id}, Type: {page.__class__.__name__}, Live: {page.live})')
