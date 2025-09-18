from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from home.models import ProjectPage
import os

class Command(BaseCommand):
    help = 'Check media files configuration and R2 connection'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== MEDIA FILES DIAGNOSIS ===")
            
            # 1. Проверяем настройки хранилища
            self.stdout.write("\n--- STORAGE SETTINGS ---")
            self.stdout.write(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
            self.stdout.write(f"MEDIA_URL: {settings.MEDIA_URL}")
            self.stdout.write(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
            
            # 2. Проверяем R2 настройки
            self.stdout.write("\n--- R2/CLOUDFLARE SETTINGS ---")
            self.stdout.write(f"AWS_ACCESS_KEY_ID: {'SET' if settings.AWS_ACCESS_KEY_ID else 'NOT SET'}")
            self.stdout.write(f"AWS_SECRET_ACCESS_KEY: {'SET' if settings.AWS_SECRET_ACCESS_KEY else 'NOT SET'}")
            self.stdout.write(f"AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}")
            self.stdout.write(f"AWS_S3_ENDPOINT_URL: {settings.AWS_S3_ENDPOINT_URL}")
            self.stdout.write(f"AWS_S3_CUSTOM_DOMAIN: {settings.AWS_S3_CUSTOM_DOMAIN}")
            self.stdout.write(f"AWS_S3_VERIFY: {settings.AWS_S3_VERIFY}")
            self.stdout.write(f"AWS_S3_REGION_NAME: {settings.AWS_S3_REGION_NAME}")
            
            # 3. Проверяем подключение к хранилищу
            self.stdout.write("\n--- STORAGE CONNECTION TEST ---")
            try:
                # Пробуем получить список файлов
                files = default_storage.listdir('')
                self.stdout.write(f"Storage connection: SUCCESS")
                self.stdout.write(f"Files in root: {len(files[1]) if files else 0}")
            except Exception as e:
                self.stdout.write(f"Storage connection: FAILED - {e}")
            
            # 4. Проверяем медиа файлы в проектах
            self.stdout.write("\n--- PROJECT MEDIA FILES ---")
            projects = ProjectPage.objects.all()
            for project in projects:
                self.stdout.write(f"\nProject: {project.title}")
                
                # Проверяем thumbnail_image
                if project.thumbnail_image:
                    self.stdout.write(f"  Thumbnail: {project.thumbnail_image.name}")
                    self.stdout.write(f"  Thumbnail URL: {project.thumbnail_image.url}")
                    try:
                        exists = default_storage.exists(project.thumbnail_image.name)
                        self.stdout.write(f"  Thumbnail exists: {exists}")
                    except Exception as e:
                        self.stdout.write(f"  Thumbnail check error: {e}")
                
                # Проверяем preview_video
                if project.preview_video:
                    self.stdout.write(f"  Preview Video: {project.preview_video.name}")
                    self.stdout.write(f"  Preview Video URL: {project.preview_video.url}")
                    try:
                        exists = default_storage.exists(project.preview_video.name)
                        self.stdout.write(f"  Preview Video exists: {exists}")
                    except Exception as e:
                        self.stdout.write(f"  Preview Video check error: {e}")
                
                # Проверяем body блоки с изображениями
                if hasattr(project, 'body') and project.body:
                    for block in project.body:
                        if block.block_type == 'image' and block.value:
                            image = block.value
                            if hasattr(image, 'image'):
                                self.stdout.write(f"  Body Image: {image.image.name}")
                                self.stdout.write(f"  Body Image URL: {image.image.url}")
                                try:
                                    exists = default_storage.exists(image.image.name)
                                    self.stdout.write(f"  Body Image exists: {exists}")
                                except Exception as e:
                                    self.stdout.write(f"  Body Image check error: {e}")
            
            # 5. Тест загрузки файла
            self.stdout.write("\n--- UPLOAD TEST ---")
            try:
                test_content = b"test file content"
                test_filename = "test_upload.txt"
                default_storage.save(test_filename, test_content)
                self.stdout.write(f"Upload test: SUCCESS - {test_filename}")
                
                # Проверяем, что файл существует
                exists = default_storage.exists(test_filename)
                self.stdout.write(f"File exists after upload: {exists}")
                
                # Удаляем тестовый файл
                default_storage.delete(test_filename)
                self.stdout.write("Test file deleted")
                
            except Exception as e:
                self.stdout.write(f"Upload test: FAILED - {e}")
            
            # 6. Рекомендации
            self.stdout.write("\n--- RECOMMENDATIONS ---")
            if not settings.AWS_ACCESS_KEY_ID:
                self.stdout.write("❌ AWS_ACCESS_KEY_ID not set - R2 won't work")
            if not settings.AWS_SECRET_ACCESS_KEY:
                self.stdout.write("❌ AWS_SECRET_ACCESS_KEY not set - R2 won't work")
            if not settings.AWS_STORAGE_BUCKET_NAME:
                self.stdout.write("❌ AWS_STORAGE_BUCKET_NAME not set - R2 won't work")
            if not settings.AWS_S3_ENDPOINT_URL:
                self.stdout.write("❌ AWS_S3_ENDPOINT_URL not set - R2 won't work")
            
            if all([settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, 
                   settings.AWS_STORAGE_BUCKET_NAME, settings.AWS_S3_ENDPOINT_URL]):
                self.stdout.write("✅ All R2 environment variables are set")
            
            self.stdout.write(self.style.SUCCESS("\n=== MEDIA DIAGNOSIS COMPLETE ==="))
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during media diagnosis: {e}')
            )
