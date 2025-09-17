from django.contrib import admin
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.snippets.models import register_snippet

from .models import SocialLink


# Регистрируем модель SocialLink как Wagtail Snippet
register_snippet(SocialLink)


# Регистрируем настройки контактов как Wagtail Setting
@register_setting
class ContactSetting(BaseSiteSetting):
    """Настройки для контактного виджета в Wagtail"""
    
    # Основная кнопка виджета
    main_button_icon = models.FileField(
        upload_to='contact_icons/',
        verbose_name="Иконка основной кнопки",
        help_text="SVG иконка для основной кнопки виджета (по умолчанию send.svg)",
        default='contact_icons/send.svg'
    )
    
    # Настройки отображения
    widget_enabled = models.BooleanField(
        default=True,
        verbose_name="Включить виджет",
        help_text="Показывать ли контактный виджет на сайте"
    )
    
    # Позиция виджета
    POSITION_CHOICES = [
        ('bottom-right', 'Правый нижний угол'),
        ('bottom-left', 'Левый нижний угол'),
    ]
    
    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='bottom-right',
        verbose_name="Позиция",
        help_text="Позиция виджета на странице"
    )

    class Meta:
        verbose_name = "Настройки контактов"
        verbose_name_plural = "Настройки контактов"

    panels = [
        FieldPanel('widget_enabled'),
        FieldPanel('main_button_icon'),
        FieldPanel('position'),
    ]
