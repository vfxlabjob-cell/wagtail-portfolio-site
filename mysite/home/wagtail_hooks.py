from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetChooserViewSet
from wagtail import hooks
from django.utils.text import slugify
from django.templatetags.static import static
from django.utils.html import format_html
from .models import Video, ProjectCategory, ProjectPage


class VideoChooserViewSet(SnippetChooserViewSet):
    """
    Это кастомный Chooser ViewSet, который говорит Wagtail,
    как должна выглядеть форма загрузки в модальном окне.
    """
    model = Video
    # Указываем поля, которые будут в форме на вкладке "Upload"
    form_fields = ['title', 'file']


class VideoViewSet(SnippetViewSet):
    """
    Это основной ViewSet, который управляет моделью Video.
    Он отвечает за меню, список, редактирование И ЗА ТО,
    КАКОЙ WIDGET ВЫБОРА (CHOOSER) ИСПОЛЬЗОВАТЬ.
    """
    model = Video
    icon = "media"
    menu_label = "Videos"
    menu_order = 230
    add_to_admin_menu = True
    list_display = ("title",)
    search_fields = ("title",)

    # --- САМАЯ ГЛАВНАЯ СТРОКА ---
    # Мы явно указываем, что для виджета выбора (chooser)
    # нужно использовать наш кастомный ViewSet с формой загрузки.
    chooser_viewset_class = VideoChooserViewSet


# Регистрируем наш финальный, настроенный ViewSet
register_snippet(VideoViewSet)


@hooks.register('before_create_snippet')
def auto_generate_slug_for_category(request, instance):
    """Автоматически создаем slug для ProjectCategory"""
    if isinstance(instance, ProjectCategory):
        if not instance.slug and instance.name:
            instance.slug = slugify(instance.name)
            print(f"✅ Auto-generated slug for ProjectCategory: {instance.name} -> {instance.slug}")


@hooks.register('before_edit_snippet')
def auto_generate_slug_for_category_edit(request, instance):
    """Автоматически создаем slug для ProjectCategory при редактировании"""
    if isinstance(instance, ProjectCategory):
        if not instance.slug and instance.name:
            instance.slug = slugify(instance.name)
            print(f"✅ Auto-generated slug for ProjectCategory (edit): {instance.name} -> {instance.slug}")


@hooks.register('before_create_page')
def auto_generate_slug_for_project_page(request, parent, page_class):
    """Автоматически создаем slug для ProjectPage"""
    if page_class == ProjectPage:
        if not page_class.slug and page_class.title:
            page_class.slug = slugify(page_class.title)
            print(f"✅ Auto-generated slug for ProjectPage: {page_class.title} -> {page_class.slug}")


@hooks.register('insert_global_admin_js')
def global_admin_js():
    """Добавляем JavaScript для автоматического создания slug"""
    return format_html(
        '<script src="{}"></script>',
        static('js/admin-slug-auto.js')
    )