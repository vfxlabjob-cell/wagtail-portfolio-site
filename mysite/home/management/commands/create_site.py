from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage


class Command(BaseCommand):
    help = 'Create site with PortfolioIndexPage as root'

    def handle(self, *args, **options):
        self.stdout.write("=== CREATING SITE (TEST DEPLOY) ===")
        
        try:
            # 1. Находим Portfolio страницу
            portfolio_page = PortfolioIndexPage.objects.filter(slug="home").first()
            if not portfolio_page:
                # Создаем Portfolio страницу если её нет
                root_page = Page.objects.filter(depth=1).first()
                if root_page:
                    portfolio_page = PortfolioIndexPage(
                        title="Portfolio",
                        slug="home",
                        intro='Welcome to my creative portfolio'
                    )
                    root_page.add_child(instance=portfolio_page)
                    portfolio_page.live = True
                    portfolio_page.save()
                    self.stdout.write(self.style.SUCCESS(f'✅ Created Portfolio page: {portfolio_page.title}'))
                else:
                    self.stdout.write(self.style.ERROR('❌ No root page found'))
                    return
            
            # 2. Удаляем все существующие сайты
            Site.objects.all().delete()
            self.stdout.write('🗑️ Deleted all existing sites')
            
            # 3. Создаем новый сайт
            site = Site.objects.create(
                hostname='web-production-b4d2a.up.railway.app',
                port=443,
                root_page=portfolio_page,
                is_default_site=True,
                site_name='Portfolio Site'
            )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Created site: {site.site_name}'))
            self.stdout.write(f'   Hostname: {site.hostname}')
            self.stdout.write(f'   Root page: {site.root_page.title}')
            self.stdout.write(f'   Is default: {site.is_default_site}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
            import traceback
            traceback.print_exc()
        
        self.stdout.write("=== SITE CREATION COMPLETE ===")
