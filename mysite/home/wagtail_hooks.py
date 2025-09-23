from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.html import format_html
from wagtail.admin.menu import MenuItem
from wagtail.admin.views import generic
from wagtail import hooks
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json


@hooks.register('register_admin_menu_item')
def register_cleanup_menu_item():
    """Добавляем пункт меню для очистки медиафайлов"""
    return MenuItem(
        'Cleanup Media',
        '/admin/cleanup-media/',
        classnames='icon icon-bin',
        order=1000
    )


@hooks.register('register_admin_urls')
def register_cleanup_urls():
    """Регистрируем URL для страницы очистки"""
    return [
        path('cleanup-media/', cleanup_media_view, name='cleanup_media'),
        path('cleanup-media/check/', check_unused_files, name='check_unused_files'),
        path('cleanup-media/delete/', delete_unused_files, name='delete_unused_files'),
    ]


def cleanup_media_view(request):
    """Страница очистки медиафайлов"""
    if request.method == 'POST':
        # Здесь будет логика очистки
        pass
    
    return render(request, 'admin/cleanup_media.html', {
        'title': 'Cleanup Unused Media Files',
    })


@require_http_methods(["GET"])
def check_unused_files(request):
    """API для проверки неиспользуемых файлов"""
    from wagtail.images.models import Image
    from wagtail.documents.models import Document
    from wagtail.models import Page
    
    # Получаем все используемые файлы
    used_files = set()
    
    # Проверяем все страницы
    for page in Page.objects.all():
        if hasattr(page, 'body'):
            for block in page.body:
                if hasattr(block.value, 'get'):
                    if 'image' in block.value:
                        image = block.value['image']
                        if image:
                            used_files.add(image.file.name)
                    
                    if 'video' in block.value:
                        video = block.value['video']
                        if video:
                            used_files.add(video.file.name)
        
        # Проверяем thumbnail_image
        if hasattr(page, 'thumbnail_image') and page.thumbnail_image:
            used_files.add(page.thumbnail_image.file.name)
    
    # Получаем все файлы
    all_images = Image.objects.all()
    all_documents = Document.objects.all()
    
    unused_images = []
    unused_documents = []
    
    for image in all_images:
        if image.file.name not in used_files:
            unused_images.append({
                'id': image.id,
                'name': image.file.name,
                'title': image.title,
                'size': image.file.size if hasattr(image.file, 'size') else 0
            })
    
    for doc in all_documents:
        if doc.file.name not in used_files:
            unused_documents.append({
                'id': doc.id,
                'name': doc.file.name,
                'title': doc.title,
                'size': doc.file.size if hasattr(doc.file, 'size') else 0
            })
    
    return JsonResponse({
        'unused_images': unused_images,
        'unused_documents': unused_documents,
        'total_unused': len(unused_images) + len(unused_documents)
    })


@require_http_methods(["POST"])
def delete_unused_files(request):
    """API для удаления неиспользуемых файлов"""
    from wagtail.images.models import Image
    from wagtail.documents.models import Document
    
    data = json.loads(request.body)
    image_ids = data.get('image_ids', [])
    document_ids = data.get('document_ids', [])
    
    deleted_count = 0
    
    # Удаляем изображения
    for image_id in image_ids:
        try:
            image = Image.objects.get(id=image_id)
            image.delete()
            deleted_count += 1
        except Image.DoesNotExist:
            pass
    
    # Удаляем документы
    for doc_id in document_ids:
        try:
            doc = Document.objects.get(id=doc_id)
            doc.delete()
            deleted_count += 1
        except Document.DoesNotExist:
            pass
    
    return JsonResponse({
        'success': True,
        'deleted_count': deleted_count
    })