from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage, ProjectCategory, Video
import json
import os

class Command(BaseCommand):
    help = 'Simple import of site data - creates content from scratch'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== SIMPLE SITE DATA IMPORT ===")

            # Путь к файлу экспорта
            export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..', 'exported_data')
            all_data_file = os.path.join(export_dir, 'all_site_data.json')

            if not os.path.exists(all_data_file):
                self.stdout.write(self.style.ERROR(f'Export file not found: {all_data_file}'))
                self.stdout.write("Please run 'export_site_data' command first on your local machine")
                return

            # Читаем данные
            with open(all_data_file, 'r', encoding='utf-8') as f:
                all_data = json.load(f)

            self.stdout.write("=== CLEANING EXISTING DATA ===")

            # Удаляем все кастомные страницы
            PortfolioIndexPage.objects.all().delete()
            self.stdout.write("Deleted all portfolio pages")

            # Удаляем категории и видео
            ProjectCategory.objects.all().delete()
            Video.objects.all().delete()
            self.stdout.write("Deleted all categories and videos")

            self.stdout.write("=== CREATING NEW CONTENT ===")

            # 1. Создаем категории
            if 'categories' in all_data and all_data['categories']:
                self.stdout.write("Creating categories...")
                for cat_data in all_data['categories']:
                    category = ProjectCategory(
                        name=cat_data['fields']['name'],
                        description=cat_data['fields'].get('description', ''),
                        slug=cat_data['fields'].get('slug', cat_data['fields']['name'].lower().replace(' ', '-'))
                    )
                    category.save()
                    self.stdout.write(f"Created category: {category.name}")

            # 2. Создаем видео
            if 'videos' in all_data and all_data['videos']:
                self.stdout.write("Creating videos...")
                for video_data in all_data['videos']:
                    fields = video_data['fields']

                    # Находим категорию по имени
                    category = None
                    if fields.get('category'):
                        try:
                            # Ищем категорию среди созданных
                            for cat_data in all_data['categories']:
                                if cat_data['pk'] == fields['category']:
                                    category = ProjectCategory.objects.filter(name=cat_data['fields']['name']).first()
                                    break
                        except:
                            pass

                    video = Video(
                        title=fields['title'],
                        description=fields.get('description', ''),
                        youtube_url=fields.get('youtube_url', ''),
                        vimeo_url=fields.get('vimeo_url', ''),
                        video_file_url=fields.get('video_file_url', ''),
                        thumbnail_url=fields.get('thumbnail_url', ''),
                        duration=fields.get('duration', 0),
                        created_at=fields.get('created_at', '2024-01-01T00:00:00Z'),
                        category=category
                    )
                    video.save()
                    self.stdout.write(f"Created video: {video.title}")

            # 3. Создаем главную страницу
            if 'pages' in all_data and all_data['pages']:
                self.stdout.write("Creating home page...")

                # Находим корневую страницу для добавления нашей домашней страницы
                root = Page.objects.filter(depth=2).first()  # Welcome page
                if not root:
                    root = Page.objects.get(depth=1)  # Root page

                # Ищем данные домашней страницы
                home_page_data = None
                for page_data in all_data['pages']:
                    if page_data['model'] == 'home.homepage':
                        home_page_data = page_data
                        break

                if home_page_data:
                    fields = home_page_data['fields']

                    # Создаем новую портфолио страницу
                    portfolio_page = PortfolioIndexPage(
                        title=fields.get('title', 'Portfolio Site'),
                        slug=fields.get('slug', 'home'),
                        seo_title=fields.get('seo_title', ''),
                        search_description=fields.get('search_description', ''),
                        show_in_menus=fields.get('show_in_menus', True),
                        intro=fields.get('intro', 'Welcome to my portfolio'),
                        live=True,
                        has_unpublished_changes=False
                    )

                    # Добавляем как дочернюю к корневой странице
                    root.add_child(instance=portfolio_page)
                    portfolio_page.save_revision().publish()

                    self.stdout.write(f"Created portfolio page: {portfolio_page.title}")

                    # Устанавливаем как корневую страницу сайта
                    site = Site.objects.get(is_default_site=True)
                    site.root_page = portfolio_page
                    site.save()
                    self.stdout.write("Set as default site root page")

                else:
                    # Создаем базовую портфолио страницу
                    portfolio_page = PortfolioIndexPage(
                        title='Portfolio Site',
                        slug='home',
                        intro='Welcome to my portfolio',
                        live=True,
                        has_unpublished_changes=False
                    )
                    root.add_child(instance=portfolio_page)
                    portfolio_page.save_revision().publish()

                    # Устанавливаем как корневую страницу сайта
                    site = Site.objects.get(is_default_site=True)
                    site.root_page = portfolio_page
                    site.save()
                    self.stdout.write("Created default portfolio page")

            # 4. Показываем статистику
            self.stdout.write("\n=== IMPORT STATISTICS ===")
            self.stdout.write(f"Total pages: {Page.objects.count()}")
            self.stdout.write(f"Total portfolio pages: {PortfolioIndexPage.objects.count()}")
            self.stdout.write(f"Total categories: {ProjectCategory.objects.count()}")
            self.stdout.write(f"Total videos: {Video.objects.count()}")
            self.stdout.write(f"Total sites: {Site.objects.count()}")

            # 5. Показываем созданные страницы
            self.stdout.write("\n=== CREATED PAGES ===")
            for page in PortfolioIndexPage.objects.all():
                self.stdout.write(f"- {page.title} (ID: {page.id}, Live: {page.live})")

            self.stdout.write(self.style.SUCCESS("\n=== SIMPLE IMPORT COMPLETE ==="))
            self.stdout.write("Your site should now be accessible with imported content!")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during simple import: {e}')
            )
            import traceback
            self.stdout.write(traceback.format_exc())
