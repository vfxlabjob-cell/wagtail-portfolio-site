from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetChooserViewSet
from .models import Video


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