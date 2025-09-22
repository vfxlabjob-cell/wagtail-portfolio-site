from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage

class Command(BaseCommand):
    help = 'Fix home page to be Portfolio index page'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== FIXING HOME PAGE ===")
            
            # 1. Находим корневую страницу
            root_page = Page.objects.filter(depth=1).first()
            if not root_page:
                self.stdout.write(self.style.ERROR("No root page found!"))
                return
            
            # 2. Удаляем стандартную страницу Wagtail "Welcome to your new Wagtail site"
            default_home = Page.objects.filter(slug="home").exclude(content_type__model='portfolioindexpage').first()
            if default_home:
                self.stdout.write(f'Found default Wagtail page: {default_home.title}')
                default_home.delete()
                self.stdout.write(self.style.SUCCESS('Deleted default Wagtail home page'))
            
            # 3. Создаем или находим PortfolioIndexPage
            portfolio_page = PortfolioIndexPage.objects.filter(slug="home").first()
            if not portfolio_page:
                portfolio_page = PortfolioIndexPage(
                    title="Portfolio",
                    slug="home",
                    intro='Welcome to my creative portfolio'
                )
                root_page.add_child(instance=portfolio_page)
                self.stdout.write(self.style.SUCCESS(f'Created Portfolio home page: {portfolio_page.title}'))
            else:
                # Обновляем название если нужно
                if portfolio_page.title != "Portfolio":
                    portfolio_page.title = "Portfolio"
                    portfolio_page.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated home page title to: {portfolio_page.title}'))
                else:
                    self.stdout.write(f'Portfolio home page already exists: {portfolio_page.title}')
            
            # 4. Убеждаемся, что страница опубликована
            if not portfolio_page.live:
                portfolio_page.live = True
                portfolio_page.save()
                self.stdout.write(self.style.SUCCESS('Published Portfolio home page'))
            
            # 5. Обновляем настройки сайта
            site = Site.objects.first()
            if site:
                site.root_page = portfolio_page
                site.save()
                self.stdout.write(self.style.SUCCESS(f'Updated site root to: {portfolio_page.title}'))
            else:
                site = Site.objects.create(
                    hostname='localhost',
                    port=8000,
                    root_page=portfolio_page,
                    is_default_site=True
                )
                self.stdout.write(self.style.SUCCESS(f'Created site: {site.hostname}:{site.port} -> {portfolio_page.title}'))
            
            self.stdout.write(self.style.SUCCESS("\n=== HOME PAGE FIXED ==="))
            self.stdout.write(f"Home page: {portfolio_page.title}")
            self.stdout.write(f"URL: {portfolio_page.url}")
            self.stdout.write(f"Live: {portfolio_page.live}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            import traceback
            traceback.print_exc()
