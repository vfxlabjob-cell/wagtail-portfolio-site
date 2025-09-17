from django.db import models
from wagtail.admin.panels import FieldPanel


class SocialLink(models.Model):
    """Модель для хранения ссылок на социальные сети"""
    
    name = models.CharField(
        max_length=50,
        verbose_name="Название",
        help_text="Название социальной сети (например: Instagram, Telegram)"
    )
    
    icon = models.FileField(
        upload_to='contact_icons/',
        verbose_name="Иконка",
        help_text="SVG иконка для социальной сети"
    )
    
    url = models.URLField(
        verbose_name="Ссылка",
        help_text="Полная ссылка на профиль/канал"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
        help_text="Показывать ли эту ссылку в виджете"
    )
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
        help_text="Порядок отображения (меньше число = выше в списке)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
        FieldPanel('url'),
        FieldPanel('is_active'),
        FieldPanel('order'),
    ]