from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage

class Command(BaseCommand):
    help = 'Create home page'

    def handle(self, *args, **options):
        try:
            # Находим корневую страницу
            root = Page.objects.filter(depth=1).first()
            if not root:
                self.stdout.write(self.style.ERROR("No root page found!"))
                return
            
            # Проверяем, есть ли уже главная страница
            existing_home = PortfolioIndexPage.objects.filter(slug='home').first()
            if existing_home:
                self.stdout.write(f'Home page already exists: {existing_home.title}')
                return
            
            # Создаем главную страницу
            home_page = PortfolioIndexPage(
                title='Home',
                slug='home',
                intro='Welcome to our portfolio!'
            )
            
            # Добавляем как дочернюю страницу
            root.add_child(instance=home_page)
            self.stdout.write(self.style.SUCCESS(f'Created home page: {home_page.title}'))
            
            # Создаем или обновляем настройки сайта
            site = Site.objects.first()
            if site:
                site.root_page = home_page
                site.save()
                self.stdout.write(f'Updated site root to: {home_page.title}')
            else:
                site = Site.objects.create(
                    hostname='127.0.0.1',
                    port=8000,
                    root_page=home_page,
                    is_default_site=True
                )
                self.stdout.write(f'Created site: {site.hostname}:{site.port} -> {home_page.title}')
            
            self.stdout.write(self.style.SUCCESS('Home page setup complete!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))

