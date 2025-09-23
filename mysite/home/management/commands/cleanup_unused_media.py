from django.core.management.base import BaseCommand
from django.db.models import Q
from wagtail.images.models import Image
from wagtail.documents.models import Document
from wagtail.embeds.models import Embed
from wagtail.models import Page
from wagtail.rich_text import RichText
import re


class Command(BaseCommand):
    help = 'Clean up unused media files from Cloudflare R2'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No files will be deleted'))
        
        self.stdout.write("=== CLEANING UP UNUSED MEDIA FILES ===")
        
        # Получаем все используемые файлы
        used_files = set()
        
        # 1. Изображения в StreamField блоках
        for page in Page.objects.all():
            if hasattr(page, 'body'):
                for block in page.body:
                    if hasattr(block.value, 'get'):
                        # Проверяем различные типы блоков
                        if 'image' in block.value:
                            image = block.value['image']
                            if image:
                                used_files.add(image.file.name)
                        
                        if 'video' in block.value:
                            video = block.value['video']
                            if video:
                                used_files.add(video.file.name)
        
        # 2. Изображения в RichTextField
        for page in Page.objects.all():
            for field in page._meta.get_fields():
                if hasattr(field, 'related_model') and field.related_model == Image:
                    try:
                        image = getattr(page, field.name, None)
                        if image:
                            used_files.add(image.file.name)
                    except:
                        pass
        
        # 3. Thumbnail изображения
        for page in Page.objects.all():
            if hasattr(page, 'thumbnail_image') and page.thumbnail_image:
                used_files.add(page.thumbnail_image.file.name)
        
        self.stdout.write(f"Found {len(used_files)} used files")
        
        # Получаем все файлы в R2
        all_images = Image.objects.all()
        all_documents = Document.objects.all()
        
        unused_images = []
        unused_documents = []
        
        # Проверяем изображения
        for image in all_images:
            if image.file.name not in used_files:
                unused_images.append(image)
        
        # Проверяем документы
        for doc in all_documents:
            if doc.file.name not in used_files:
                unused_documents.append(doc)
        
        self.stdout.write(f"Unused images: {len(unused_images)}")
        self.stdout.write(f"Unused documents: {len(unused_documents)}")
        
        if not dry_run:
            # Удаляем неиспользуемые файлы
            for image in unused_images:
                self.stdout.write(f"Deleting unused image: {image.file.name}")
                image.delete()
            
            for doc in unused_documents:
                self.stdout.write(f"Deleting unused document: {doc.file.name}")
                doc.delete()
            
            self.stdout.write(self.style.SUCCESS(f"Deleted {len(unused_images)} images and {len(unused_documents)} documents"))
        else:
            self.stdout.write("Files that would be deleted:")
            for image in unused_images:
                self.stdout.write(f"  - Image: {image.file.name}")
            for doc in unused_documents:
                self.stdout.write(f"  - Document: {doc.file.name}")
        
        self.stdout.write("=== CLEANUP COMPLETE ===")
