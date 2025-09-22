from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.models import Page, Site
from django.contrib.contenttypes.models import ContentType
from home.models import PortfolioIndexPage


class Command(BaseCommand):
    help = 'Clean up database from old HomePage references and prepare for fresh import'

    def handle(self, *args, **options):
        self.stdout.write("=== DATABASE CLEANUP ===")
        
        try:
            with transaction.atomic():
                # 0. Удаляем все тестовые изображения чтобы пересоздать их
                self.stdout.write("Removing test images to recreate them...")
                from wagtail.images.models import Image
                test_images = Image.objects.filter(title__startswith='portfolio-thumb-')
                deleted_images = test_images.count()
                test_images.delete()
                self.stdout.write(f"Deleted {deleted_images} test images")
                
                # 1. Удаляем все страницы с несуществующими content_type
                self.stdout.write("Removing pages with missing content types...")
                
                # Находим все content_type для home app
                home_content_types = ContentType.objects.filter(app_label='home')
                valid_models = [ct.model for ct in home_content_types]
                self.stdout.write(f"Valid home models: {valid_models}")
                
                # Находим проблемные страницы
                problematic_pages = Page.objects.filter(
                    content_type__app_label='home'
                ).exclude(
                    content_type__model__in=valid_models
                )
                
                self.stdout.write(f"Found {problematic_pages.count()} problematic pages")
                for page in problematic_pages:
                    self.stdout.write(f"  - Page ID {page.id}: {page.title} (type: {page.content_type})")
                
                # Удаляем проблемные страницы
                deleted_count = problematic_pages.count()
                problematic_pages.delete()
                self.stdout.write(f"Deleted {deleted_count} problematic pages")
                
                # 2. Удаляем несуществующие content_type
                self.stdout.write("Removing obsolete content types...")
                obsolete_ct = ContentType.objects.filter(
                    app_label='home',
                    model='homepage'
                )
                if obsolete_ct.exists():
                    self.stdout.write(f"Deleting obsolete content type: homepage")
                    obsolete_ct.delete()
                
                # 3. Проверяем текущую структуру страниц
                self.stdout.write("\n=== CURRENT PAGE STRUCTURE ===")
                all_pages = Page.objects.all().order_by('path')
                for page in all_pages:
                    indent = "  " * (page.depth - 1)
                    self.stdout.write(f"{indent}- {page.title} (ID: {page.id}, Type: {page.content_type}, Depth: {page.depth})")
                
                # 4. Проверяем Site настройки
                self.stdout.write("\n=== SITE CONFIGURATION ===")
                sites = Site.objects.all()
                for site in sites:
                    self.stdout.write(f"Site: {site.hostname} -> Root page: {site.root_page.title} (ID: {site.root_page.id})")
                    
                    # Если root_page ссылается на несуществующую модель, исправляем
                    if not hasattr(site.root_page, 'specific'):
                        self.stdout.write("  WARNING: Root page has invalid content type!")
                        # Устанавливаем корневую страницу Wagtail
                        root_page = Page.objects.get(depth=1)
                        site.root_page = root_page
                        site.save()
                        self.stdout.write(f"  Fixed: Set root page to {root_page.title}")
                
                self.stdout.write(self.style.SUCCESS("\n=== CLEANUP COMPLETE ==="))
                self.stdout.write("Database is now clean and ready for import!")
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during cleanup: {e}')
            )
            import traceback
            self.stdout.write(traceback.format_exc())
