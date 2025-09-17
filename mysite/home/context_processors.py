from .models import InfoIndexPage


def info_pages(request):
    """Добавляет список информационных страниц в контекст всех шаблонов"""
    try:
        # Находим InfoIndexPage
        info_index = InfoIndexPage.objects.live().first()
        if info_index:
            # Получаем все дочерние информационные страницы
            info_pages = info_index.get_children().live().order_by('title')
            return {'info_pages': info_pages}
    except:
        pass
    
    return {'info_pages': []}
