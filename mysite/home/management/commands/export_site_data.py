from django.core.management.base import BaseCommand
from django.core import serializers
from wagtail.models import Page, Site
from home.models import ProjectCategory, Video
import json
import os

class Command(BaseCommand):
    help = 'Export all site data to JSON file'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== EXPORTING SITE DATA ===")
            
            # Создаем директорию для экспорта
            export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..', 'exported_data')
            os.makedirs(export_dir, exist_ok=True)
            
            # 1. Экспортируем все страницы
            pages = Page.objects.all()
            pages_data = serializers.serialize('json', pages, indent=2)
            
            pages_file = os.path.join(export_dir, 'pages.json')
            with open(pages_file, 'w', encoding='utf-8') as f:
                f.write(pages_data)
            
            self.stdout.write(self.style.SUCCESS(f'Exported {pages.count()} pages to {pages_file}'))
            
            # 2. Экспортируем категории проектов
            categories = ProjectCategory.objects.all()
            categories_data = serializers.serialize('json', categories, indent=2)
            
            categories_file = os.path.join(export_dir, 'categories.json')
            with open(categories_file, 'w', encoding='utf-8') as f:
                f.write(categories_data)
            
            self.stdout.write(self.style.SUCCESS(f'Exported {categories.count()} categories to {categories_file}'))
            
            # 3. Экспортируем видео
            videos = Video.objects.all()
            videos_data = serializers.serialize('json', videos, indent=2)
            
            videos_file = os.path.join(export_dir, 'videos.json')
            with open(videos_file, 'w', encoding='utf-8') as f:
                f.write(videos_data)
            
            self.stdout.write(self.style.SUCCESS(f'Exported {videos.count()} videos to {videos_file}'))
            
            # 4. Экспортируем сайты
            sites = Site.objects.all()
            sites_data = serializers.serialize('json', sites, indent=2)
            
            sites_file = os.path.join(export_dir, 'sites.json')
            with open(sites_file, 'w', encoding='utf-8') as f:
                f.write(sites_data)
            
            self.stdout.write(self.style.SUCCESS(f'Exported {sites.count()} sites to {sites_file}'))
            
            # 5. Создаем общий файл экспорта
            all_data = {
                'pages': json.loads(pages_data),
                'categories': json.loads(categories_data),
                'videos': json.loads(videos_data),
                'sites': json.loads(sites_data),
            }
            
            all_data_file = os.path.join(export_dir, 'all_site_data.json')
            with open(all_data_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)
            
            self.stdout.write(self.style.SUCCESS(f'Created complete export file: {all_data_file}'))
            
            # 6. Показываем статистику
            self.stdout.write("\n=== EXPORT STATISTICS ===")
            self.stdout.write(f"Total pages: {pages.count()}")
            self.stdout.write(f"Total categories: {categories.count()}")
            self.stdout.write(f"Total videos: {videos.count()}")
            self.stdout.write(f"Total sites: {sites.count()}")
            
            # 7. Показываем детали страниц
            self.stdout.write("\n=== PAGE DETAILS ===")
            for page in pages:
                self.stdout.write(f"- {page.title} (ID: {page.id}, Type: {page.__class__.__name__}, Live: {page.live})")
            
            self.stdout.write(self.style.SUCCESS("\n=== EXPORT COMPLETE ==="))
            self.stdout.write(f"All data exported to: {export_dir}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error exporting data: {e}')
            )
