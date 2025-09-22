from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage, CardsIndexPage, ProjectPage, ProjectCategory, Video
import json
import os

class Command(BaseCommand):
    help = 'Simple import of site data - creates content from scratch'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== SIMPLE SITE DATA IMPORT ===")

            # Путь к файлу экспорта
            export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..', 'exported_data')

            # Проверяем отдельные файлы
            categories_file = os.path.join(export_dir, 'categories.json')
            videos_file = os.path.join(export_dir, 'videos.json')

            self.stdout.write("=== CLEANING EXISTING DATA ===")

            # Удаляем все кастомные страницы
            ProjectPage.objects.all().delete()
            CardsIndexPage.objects.all().delete()
            PortfolioIndexPage.objects.all().delete()
            self.stdout.write("Deleted all portfolio pages")

            # Удаляем категории и видео
            ProjectCategory.objects.all().delete()
            Video.objects.all().delete()
            self.stdout.write("Deleted all categories and videos")

            self.stdout.write("=== CREATING NEW CONTENT ===")

            # 1. Создаем категории
            if os.path.exists(categories_file):
                self.stdout.write("Creating categories...")
                with open(categories_file, 'r', encoding='utf-8') as f:
                    categories_data = json.load(f)

                for cat_data in categories_data:
                    fields = cat_data['fields']
                    category = ProjectCategory(
                        name=fields['name'],
                        slug=fields['slug'],
                        main_text=fields.get('main_text', ''),
                        secondary_text=fields.get('secondary_text', ''),
                        seo_title=fields.get('seo_title', ''),
                        search_description=fields.get('search_description', '')
                    )
                    category.save()
                    self.stdout.write(f"Created category: {category.name}")

            # 2. Создаем видео
            if os.path.exists(videos_file):
                self.stdout.write("Creating videos...")
                with open(videos_file, 'r', encoding='utf-8') as f:
                    videos_data = json.load(f)

                for video_data in videos_data:
                    fields = video_data['fields']
                    video = Video(
                        title=fields['title']
                    )
                    # Не добавляем file, так как он будет в R2
                    video.save()
                    self.stdout.write(f"Created video: {video.title}")

            # 3. Создаем структуру страниц
            self.stdout.write("Creating page structure...")

            # Находим корневую страницу для добавления нашей структуры
            root = Page.objects.filter(depth=2).first()  # Welcome page
            if not root:
                root = Page.objects.get(depth=1)  # Root page

            # Создаем главную портфолио страницу
            portfolio_page = PortfolioIndexPage(
                title='Portfolio Site',
                slug='portfolio',
                intro='Welcome to my video portfolio',
                live=True,
                has_unpublished_changes=False
            )
            root.add_child(instance=portfolio_page)
            portfolio_page.save_revision().publish()
            self.stdout.write(f"Created portfolio page: {portfolio_page.title}")

            # Создаем страницу Cards Index
            cards_page = CardsIndexPage(
                title='Projects',
                slug='projects',
                intro='Browse my video projects by category',
                live=True,
                has_unpublished_changes=False
            )
            portfolio_page.add_child(instance=cards_page)
            cards_page.save_revision().publish()
            self.stdout.write(f"Created cards index page: {cards_page.title}")

            # Создаем несколько примеров проектов для каждой категории
            video_ads_category = ProjectCategory.objects.filter(slug='video-ads').first()
            wedding_category = ProjectCategory.objects.filter(slug='wedding-video').first()

            if video_ads_category:
                for i in range(3):
                    project = ProjectPage(
                        title=f'Video Ad Project {i+1}',
                        slug=f'video-ad-project-{i+1}',
                        category=video_ads_category,
                        live=True,
                        has_unpublished_changes=False
                    )
                    cards_page.add_child(instance=project)
                    project.save_revision().publish()
                    self.stdout.write(f"Created project: {project.title}")

            if wedding_category:
                for i in range(3):
                    project = ProjectPage(
                        title=f'Wedding Video {i+1}',
                        slug=f'wedding-video-{i+1}',
                        category=wedding_category,
                        live=True,
                        has_unpublished_changes=False
                    )
                    cards_page.add_child(instance=project)
                    project.save_revision().publish()
                    self.stdout.write(f"Created project: {project.title}")

            # Устанавливаем портфолио как корневую страницу сайта
            site = Site.objects.get(is_default_site=True)
            site.root_page = portfolio_page
            site.save()
            self.stdout.write("Set portfolio page as default site root")

            # 4. Показываем статистику
            self.stdout.write("\n=== IMPORT STATISTICS ===")
            self.stdout.write(f"Total pages: {Page.objects.count()}")
            self.stdout.write(f"Total portfolio pages: {PortfolioIndexPage.objects.count()}")
            self.stdout.write(f"Total cards pages: {CardsIndexPage.objects.count()}")
            self.stdout.write(f"Total project pages: {ProjectPage.objects.count()}")
            self.stdout.write(f"Total categories: {ProjectCategory.objects.count()}")
            self.stdout.write(f"Total videos: {Video.objects.count()}")

            # 5. Показываем созданные страницы
            self.stdout.write("\n=== CREATED PAGES ===")
            for page in PortfolioIndexPage.objects.all():
                self.stdout.write(f"- Portfolio: {page.title} (ID: {page.id})")
            for page in CardsIndexPage.objects.all():
                self.stdout.write(f"- Cards: {page.title} (ID: {page.id})")
            for page in ProjectPage.objects.all()[:5]:  # Show first 5 projects
                self.stdout.write(f"- Project: {page.title} (Category: {page.category})")

            self.stdout.write(self.style.SUCCESS("\n=== SIMPLE IMPORT COMPLETE ==="))
            self.stdout.write("Your site should now be accessible with imported content!")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during simple import: {e}')
            )
            import traceback
            self.stdout.write(traceback.format_exc())
