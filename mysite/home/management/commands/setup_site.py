from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage

class Command(BaseCommand):
    help = 'Setup site configuration for Railway'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== SETTING UP SITE ===")
            
            # 1. Находим или создаем PortfolioIndexPage
            portfolio_page = PortfolioIndexPage.objects.filter(slug="home").first()
            if not portfolio_page:
                root = Page.objects.filter(depth=1).first()
                portfolio_page = PortfolioIndexPage(
                    title="Portfolio",
                    slug="home",
                    intro='Welcome to my creative portfolio'
                )
                root.add_child(instance=portfolio_page)
                portfolio_page.live = True
                portfolio_page.save()
                self.stdout.write(self.style.SUCCESS('Created Portfolio page'))
            else:
                self.stdout.write(f'Portfolio page exists: {portfolio_page.title}')
            
            # 2. Удаляем старые сайты
            old_sites = Site.objects.all()
            for site in old_sites:
                self.stdout.write(f'Deleting old site: {site.hostname}:{site.port}')
                site.delete()
            
            # 3. Создаем новый сайт для Railway
            site = Site.objects.create(
                hostname='web-production-b4d2a.up.railway.app',
                port=80,
                root_page=portfolio_page,
                is_default_site=True
            )
            self.stdout.write(self.style.SUCCESS(f'Created site: {site.hostname} -> {portfolio_page.title}'))
            
            # 4. Убеждаемся, что страница опубликована
            if not portfolio_page.live:
                portfolio_page.live = True
                portfolio_page.save()
                self.stdout.write(self.style.SUCCESS('Published Portfolio page'))
            
            self.stdout.write(self.style.SUCCESS("\n=== SITE SETUP COMPLETE ==="))
            self.stdout.write(f"Site URL: https://{site.hostname}")
            self.stdout.write(f"Root page: {portfolio_page.title}")
            self.stdout.write(f"Page URL: {portfolio_page.url}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            import traceback
            traceback.print_exc()
