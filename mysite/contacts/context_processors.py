from .models import SocialLink


def contact_widget(request):
    """
    Контекстный процессор для передачи данных контактного виджета
    """
    return {
        'social_links': SocialLink.objects.filter(is_active=True).order_by('order', 'name')
    }
