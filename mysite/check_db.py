#!/usr/bin/env python
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.production')
django.setup()

from wagtail.models import Site, Page
from home.models import PortfolioIndexPage, ProjectPage

print("=== ПРОВЕРКА БАЗЫ ДАННЫХ ===")
print(f"Всего страниц: {Page.objects.count()}")
print(f"Всего сайтов: {Site.objects.count()}")

# Проверяем корневые страницы
root_pages = Page.objects.filter(depth=1)
print(f"Корневые страницы: {root_pages.count()}")
for page in root_pages:
    print(f"  - {page.title} (ID: {page.id})")

# Проверяем PortfolioIndexPage
portfolio_pages = PortfolioIndexPage.objects.all()
print(f"PortfolioIndexPage: {portfolio_pages.count()}")
for page in portfolio_pages:
    print(f"  - {page.title} (ID: {page.id})")

# Проверяем ProjectPage
project_pages = ProjectPage.objects.all()
print(f"ProjectPage: {project_pages.count()}")
for page in project_pages:
    print(f"  - {page.title} (ID: {page.id})")

print("=== КОНЕЦ ПРОВЕРКИ ===")
