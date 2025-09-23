import os
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet


class Video(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='videos')
    panels = [FieldPanel('title'), FieldPanel('file'),]
    def save(self, *args, **kwargs):
        if not self.title and self.file:
            filename = os.path.basename(self.file.name)
            self.title = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').capitalize()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

@register_snippet
class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, help_text="A unique, URL-friendly version of the name, e.g., 'web-design'.")
    main_text = RichTextField(blank=True, help_text="Главный текст, который будет отображаться при выборе этой категории.")
    secondary_text = RichTextField(blank=True, help_text="Второстепенный текст, который будет отображаться при выборе этой категории.")
    seo_title = models.CharField(max_length=255, blank=True, help_text="Optional. The title displayed in search engine results and browser tabs. If empty, the category name will be used.")
    search_description = models.TextField(blank=True, help_text="Optional. The short description displayed in search engine results.")
    panels = [
        FieldPanel("name"), 
        FieldPanel("slug"), 
        MultiFieldPanel([
            FieldPanel("main_text"),
            FieldPanel("secondary_text"),
        ], heading="Category Content"),
        MultiFieldPanel([FieldPanel("seo_title"), FieldPanel("search_description"),], heading="SEO Settings")
    ]
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"
        ordering = ["name"]


class BodyStreamBlock(blocks.StreamBlock):
    # --- Add Text блок ---
    add_text = blocks.StructBlock([
        ('heading', blocks.RichTextBlock(required=False, label="Heading")),
        ('paragraph', blocks.RichTextBlock(required=False, label="Paragraph")),
        ('text_align', blocks.ChoiceBlock(
            choices=[
                ('left', 'Left'),
                ('center', 'Center'),
                ('right', 'Right'),
            ],
            default='center',
            label="Text Alignment"
        )),
    ], icon="doc-full", template="blocks/add_text_block.html", label="Add Text")
    
    image = ImageChooserBlock(icon="image", template="blocks/image_block.html", label="Image")
    image_2_1 = ImageChooserBlock(icon="image", template="blocks/image_2_1_block.html", label="Image 2:1")
    video = blocks.StructBlock([
        ('video', SnippetChooserBlock('home.Video')),
        ('caption', blocks.CharBlock(required=False, label="Caption"))
    ], icon="media", template="blocks/video_block.html", label="Video")
    video_2_1 = blocks.StructBlock([
        ('video', SnippetChooserBlock('home.Video')),
        ('caption', blocks.CharBlock(required=False, label="Caption"))
    ], icon="media", template="blocks/video_2_1_block.html", label="Video 2:1")
    
    # --- Card Head 2 блок ---
    card_head_2 = blocks.StructBlock([
        ('video', SnippetChooserBlock('home.Video', icon="media", label="Video", required=True)),
        ('project_name', blocks.CharBlock(required=True, label="Project Name")),
        ('year', blocks.CharBlock(required=False, label="Year")),
        ('industry', blocks.CharBlock(required=False, label="Industry")),
        ('client_name', blocks.CharBlock(required=False, label="Client Name")),
        ('client_url', blocks.URLBlock(required=False, label="Client URL (optional)")),
    ], icon="doc-full", template="blocks/card_head_2_block.html", label="Card Head 2")
    
    # --- Смешанная галерея: изображения и видео ---
    gallery = blocks.StreamBlock([
        ('image', ImageChooserBlock(icon="image", label="Image")),
        ('video', SnippetChooserBlock('home.Video', icon="media", label="Video")),
    ], label="Media Gallery (2 to 4 items)", min_num=2, max_num=4, icon="grip", template="blocks/mixed_gallery_block.html")

    # --- ИСПРАВЛЕНО: Оставляем только ОДИН Meta класс ---
    class Meta:
        label = "Page Constructor"


class PortfolioIndexPage(Page):
    """Главная страница портфолио - здесь будут все карточки проектов"""
    intro = RichTextField(blank=True, help_text="Вводный текст для главной страницы портфолио.")
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    parent_page_types = ['wagtailcore.Page']
    subpage_types = ['home.ProjectPage', 'home.InfoIndexPage']
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_child_pages = self.get_children().live().order_by('-first_published_at')
        category_slug = request.GET.get('category')
        current_category = None
        
        # Определяем тексты для отображения
        main_text = None  # По умолчанию используем стандартный title страницы
        secondary_text = ""
        
        if category_slug:
            try:
                current_category = ProjectCategory.objects.get(slug=category_slug)
                filtered_pages = all_child_pages.filter(projectpage__category=current_category)
                # Получаем специфичные объекты ProjectPage
                context['child_pages'] = [page.specific for page in filtered_pages]
                
                # Если у категории есть свои тексты, используем их
                if current_category.main_text:
                    main_text = current_category.main_text
                if current_category.secondary_text:
                    secondary_text = current_category.secondary_text
                    
            except ProjectCategory.DoesNotExist:
                # Получаем специфичные объекты ProjectPage
                context['child_pages'] = [page.specific for page in all_child_pages]
        else:
            # Для главной страницы (All) используем intro как secondary_text
            # Получаем специфичные объекты ProjectPage
            context['child_pages'] = [page.specific for page in all_child_pages]
            if self.intro:
                secondary_text = self.intro
            
        context['categories'] = ProjectCategory.objects.all()
        context['current_category_slug'] = category_slug
        context['current_category'] = current_category
        context['display_main_text'] = main_text
        context['display_secondary_text'] = secondary_text
        return context



class ProjectPage(Page):
    category = models.ForeignKey('home.ProjectCategory', null=True, blank=True, on_delete=models.SET_NULL, related_name='projects')
    thumbnail_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="Изображение для сетки (если не выбрано видео в Card Head 2).")
    
    body = StreamField(
        BodyStreamBlock(),
        blank=True, 
        use_json_field=True,
        help_text="Основной контент страницы, собираемый из блоков."
    )
    
    content_panels = [
        # Убираем стандартное поле title, так как имя берется из Card Head блока
        FieldPanel('category'),
        FieldPanel('thumbnail_image'),
        FieldPanel('body'),
    ]
    
    def clean(self):
        super().clean()
        # Автоматически генерируем slug из title, если он не задан
        if not self.slug and self.title:
            from django.utils.text import slugify
            self.slug = slugify(self.title)

    parent_page_types = ['home.PortfolioIndexPage']
    subpage_types = []
    
    def get_thumbnail_video(self):
        """Получаем видео из Card Head 2 блока для использования в сетке"""
        # Ищем Card Head 2 блок в body
        for block in self.body:
            if block.block_type == 'card_head_2' and hasattr(block.value, 'get'):
                video = block.value.get('video')
                if video:
                    return video
        # Если Card Head 2 не найден, возвращаем None
        return None


class InfoIndexPage(Page):
    """Главная страница раздела Information Pages"""
    intro = RichTextField(blank=True, help_text="Вводный текст для раздела Information Pages.")
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('slug'),
    ]
    
    parent_page_types = ['wagtailcore.Page']  # Может быть дочерней страницей любой страницы
    subpage_types = ['home.InfoPage']
    
    def save(self, *args, **kwargs):
        # Автоматически генерируем slug из названия страницы, если он не задан
        if not self.slug or self.slug == '':
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        
        # Обновляем url_path при сохранении
        if self.get_parent():
            self.set_url_path(self.get_parent())
        
        super().save(*args, **kwargs)
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Получаем все дочерние информационные страницы
        context['info_pages'] = self.get_children().live().order_by('title')
        return context


class InfoPage(Page):
    """Отдельная информационная страница (Terms of Service, Privacy Policy, etc.)"""
    body = RichTextField(blank=True, help_text="Основной контент информационной страницы.")
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('slug'),
    ]
    
    parent_page_types = ['home.InfoIndexPage']
    subpage_types = []
    
    def save(self, *args, **kwargs):
        # Автоматически генерируем slug из названия страницы, если он не задан
        if not self.slug or self.slug == '':
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        
        # Обновляем url_path при сохранении
        if self.get_parent():
            self.set_url_path(self.get_parent())
        
        super().save(*args, **kwargs)
    
    def get_admin_display_title(self):
        """Возвращаем стандартное название страницы для админки"""
        return self.title