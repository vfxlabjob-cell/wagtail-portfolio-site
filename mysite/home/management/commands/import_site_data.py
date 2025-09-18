from django.core.management.base import BaseCommand
from django.core import serializers
from django.db import transaction
from wagtail.models import Page, Site
from home.models import ProjectCategory, Video
import json
import os

class Command(BaseCommand):
    help = 'Import site data from JSON file'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== IMPORTING SITE DATA ===")
            
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
            
            with transaction.atomic():
                # 1. Импортируем категории проектов
                if 'categories' in all_data and all_data['categories']:
                    self.stdout.write("Importing categories...")
                    for obj_data in all_data['categories']:
                        try:
                            # Удаляем pk чтобы создать новый объект
                            obj_data['pk'] = None
                            obj = serializers.deserialize('json', json.dumps([obj_data]))
                            for item in obj:
                                item.save()
                            self.stdout.write(f"Imported category: {obj_data['fields']['name']}")
                        except Exception as e:
                            self.stdout.write(f"Error importing category: {e}")
                
                # 2. Импортируем видео
                if 'videos' in all_data and all_data['videos']:
                    self.stdout.write("Importing videos...")
                    for obj_data in all_data['videos']:
                        try:
                            obj_data['pk'] = None
                            obj = serializers.deserialize('json', json.dumps([obj_data]))
                            for item in obj:
                                item.save()
                            self.stdout.write(f"Imported video: {obj_data['fields']['title']}")
                        except Exception as e:
                            self.stdout.write(f"Error importing video: {e}")
                
                # 3. Импортируем страницы
                if 'pages' in all_data and all_data['pages']:
                    self.stdout.write("Importing pages...")
                    
                    # Сначала импортируем страницы без parent_id
                    pages_to_import = all_data['pages'][:]
                    imported_pages = {}
                    
                    # Сортируем по depth для правильного порядка импорта
                    pages_to_import.sort(key=lambda x: x['fields']['depth'])
                    
                    for obj_data in pages_to_import:
                        try:
                            # Сохраняем старый pk для связи
                            old_pk = obj_data['pk']
                            obj_data['pk'] = None
                            
                            # Убираем parent_id для первого прохода
                            if 'parent_id' in obj_data['fields']:
                                del obj_data['fields']['parent_id']
                            
                            obj = serializers.deserialize('json', json.dumps([obj_data]))
                            for item in obj:
                                item.save()
                                imported_pages[old_pk] = item.object.pk
                                self.stdout.write(f"Imported page: {item.object.title} (ID: {item.object.pk})")
                        except Exception as e:
                            self.stdout.write(f"Error importing page: {e}")
                
                # 4. Импортируем сайты
                if 'sites' in all_data and all_data['sites']:
                    self.stdout.write("Importing sites...")
                    for obj_data in all_data['sites']:
                        try:
                            obj_data['pk'] = None
                            # Обновляем root_page_id если нужно
                            if 'root_page_id' in obj_data['fields'] and obj_data['fields']['root_page_id']:
                                old_root_id = obj_data['fields']['root_page_id']
                                if old_root_id in imported_pages:
                                    obj_data['fields']['root_page_id'] = imported_pages[old_root_id]
                                else:
                                    obj_data['fields']['root_page_id'] = None
                            
                            obj = serializers.deserialize('json', json.dumps([obj_data]))
                            for item in obj:
                                item.save()
                            self.stdout.write(f"Imported site: {obj_data['fields']['hostname']}")
                        except Exception as e:
                            self.stdout.write(f"Error importing site: {e}")
                
                # 5. Публикуем все страницы
                self.stdout.write("Publishing all pages...")
                unpublished_pages = Page.objects.filter(live=False)
                for page in unpublished_pages:
                    page.live = True
                    page.save()
                    self.stdout.write(f"Published: {page.title}")
            
            # 6. Показываем статистику
            self.stdout.write("\n=== IMPORT STATISTICS ===")
            self.stdout.write(f"Total pages: {Page.objects.count()}")
            self.stdout.write(f"Total categories: {ProjectCategory.objects.count()}")
            self.stdout.write(f"Total videos: {Video.objects.count()}")
            self.stdout.write(f"Total sites: {Site.objects.count()}")
            
            # 7. Показываем детали страниц
            self.stdout.write("\n=== IMPORTED PAGES ===")
            for page in Page.objects.all():
                self.stdout.write(f"- {page.title} (ID: {page.id}, Type: {page.__class__.__name__}, Live: {page.live})")
            
            self.stdout.write(self.style.SUCCESS("\n=== IMPORT COMPLETE ==="))
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing data: {e}')
            )
