from django.core.management.base import BaseCommand
from django.core import serializers
from django.db import transaction
from wagtail.models import Page, Site
from home.models import ProjectCategory, Video
import json
import os

class Command(BaseCommand):
    help = 'Import site data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clean existing data before import',
        )

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

            # Опционально очищаем базу данных
            clean_db = options.get('clean', False) or os.environ.get('CLEAN_DB', '').lower() == 'true'
            if clean_db:
                self.stdout.write("=== CLEANING DATABASE ===")

                # Удаляем все страницы кроме системных корневых (depth=1,2)
                pages_to_delete = Page.objects.exclude(depth__in=[1, 2])
                if pages_to_delete.exists():
                    self.stdout.write(f"Deleting {pages_to_delete.count()} pages...")
                    pages_to_delete.delete()

                # Удаляем все Home страницы (они будут пересозданы)
                from home.models import HomePage
                home_pages = HomePage.objects.all()
                if home_pages.exists():
                    self.stdout.write(f"Deleting {home_pages.count()} home pages...")
                    home_pages.delete()

                # Удаляем категории и видео
                categories_count = ProjectCategory.objects.count()
                videos_count = Video.objects.count()

                if categories_count > 0:
                    self.stdout.write(f"Deleting {categories_count} categories...")
                    ProjectCategory.objects.all().delete()

                if videos_count > 0:
                    self.stdout.write(f"Deleting {videos_count} videos...")
                    Video.objects.all().delete()

                self.stdout.write("Database cleaned successfully")

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
                            # Пропускаем корневые системные страницы (Root, Welcome)
                            if obj_data['fields'].get('depth', 0) <= 2:
                                continue

                            # Сохраняем старый pk для связи
                            old_pk = obj_data['pk']
                            obj_data['pk'] = None

                            # Находим родительскую страницу (обычно Welcome page с depth=2)
                            if 'parent_id' in obj_data['fields']:
                                # Ищем подходящую родительскую страницу
                                parent_page = Page.objects.filter(depth=2).first()
                                if parent_page:
                                    obj_data['fields']['parent_id'] = parent_page.id
                                else:
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
