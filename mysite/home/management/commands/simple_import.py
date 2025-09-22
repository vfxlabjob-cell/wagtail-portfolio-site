from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Page, Site
from wagtail.images.models import Image
from home.models import PortfolioIndexPage, CardsIndexPage, ProjectPage, ProjectCategory, Video
import json
import os
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage

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

            # 2.5. Создаем тестовые изображения для проектов
            self.stdout.write("Creating sample images...")
            self.create_sample_images()

            # 3. Создаем структуру страниц
            self.stdout.write("Creating page structure...")

            # Находим корневую страницу для добавления нашей структуры
            root = Page.objects.get(depth=1)  # Root page (всегда существует)
            
            # Проверяем, есть ли уже портфолио страница
            existing_portfolio = PortfolioIndexPage.objects.first()
            if existing_portfolio:
                portfolio_page = existing_portfolio
                self.stdout.write(f"Using existing portfolio page: {portfolio_page.title}")
            else:
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
            existing_cards = CardsIndexPage.objects.first()
            if existing_cards:
                cards_page = existing_cards
                self.stdout.write(f"Using existing cards page: {cards_page.title}")
            else:
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
            site, created = Site.objects.get_or_create(
                is_default_site=True,
                defaults={
                    'hostname': 'localhost',
                    'port': 80,
                    'site_name': 'Portfolio Site',
                    'root_page': portfolio_page
                }
            )
            if not created:
                site.root_page = portfolio_page
                site.save()
                self.stdout.write("Updated existing site root page")
            else:
                self.stdout.write("Created new default site with portfolio root")

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

    def create_sample_images(self):
        """Создает тестовые изображения для проектов"""
        try:
            from PIL import Image as PILImage
            from io import BytesIO
            
            # Создаем несколько тестовых изображений разных размеров
            sample_images = [
                ("portfolio-thumb-1.jpg", (800, 600), (255, 100, 100)),  # Красный
                ("portfolio-thumb-2.jpg", (800, 600), (100, 255, 100)),  # Зеленый  
                ("portfolio-thumb-3.jpg", (800, 600), (100, 100, 255)),  # Синий
                ("portfolio-thumb-4.jpg", (800, 600), (255, 255, 100)),  # Желтый
                ("portfolio-thumb-5.jpg", (800, 600), (255, 100, 255)),  # Пурпурный
                ("portfolio-thumb-6.jpg", (800, 600), (100, 255, 255)),  # Циан
            ]
            
            for filename, size, color in sample_images:
                self.stdout.write(f"Processing image: {filename}")
                # Проверяем, не существует ли уже изображение с таким именем
                if Image.objects.filter(title=filename).exists():
                    self.stdout.write(f"Image {filename} already exists, skipping")
                    continue
                    
                # Создаем изображение с помощью PIL
                self.stdout.write(f"Creating PIL image for {filename}")
                img = PILImage.new('RGB', size, color)
                
                # Добавляем текст на изображение
                try:
                    from PIL import ImageDraw, ImageFont
                    draw = ImageDraw.Draw(img)
                    text = f"Sample Image\n{filename}"
                    # Используем стандартный шрифт
                    draw.text((size[0]//2-100, size[1]//2-20), text, fill=(255, 255, 255))
                    self.stdout.write(f"Added text to {filename}")
                except ImportError:
                    # Если нет PIL, просто создаем цветной прямоугольник
                    self.stdout.write(f"PIL drawing not available for {filename}")
                    pass
                
                # Сохраняем в BytesIO
                self.stdout.write(f"Saving {filename} to BytesIO")
                img_io = BytesIO()
                img.save(img_io, format='JPEG', quality=85)
                img_io.seek(0)
                
                # Создаем Wagtail Image
                self.stdout.write(f"Creating Wagtail Image object for {filename}")
                wagtail_image = Image(
                    title=filename,
                    file=ImageFile(img_io, name=filename)
                )
                self.stdout.write(f"Saving {filename} to storage...")
                wagtail_image.save()
                self.stdout.write(f"Created sample image: {filename}")
                
        except ImportError:
            self.stdout.write("PIL not available, skipping image creation")
        except Exception as e:
            self.stdout.write(f"Error creating sample images: {e}")
            import traceback
            self.stdout.write(traceback.format_exc())
