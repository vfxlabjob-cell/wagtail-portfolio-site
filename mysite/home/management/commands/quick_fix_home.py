from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage

class Command(BaseCommand):
    help = 'Quick fix home page - delete default and create portfolio'

    def handle(self, *args, **options):
        try:
            # 1. Удаляем все страницы с slug="home" кроме PortfolioIndexPage
            default_pages = Page.objects.filter(slug="home").exclude(content_type__model='portfolioindexpage')
            for page in default_pages:
                self.stdout.write(f'Deleting: {page.title}')
                page.delete()
            
            # 2. Создаем PortfolioIndexPage если не существует
            portfolio_page = PortfolioIndexPage.objects.filter(slug="home").first()
            if not portfolio_page:
                root = Page.objects.filter(depth=1).first()
                portfolio_page = PortfolioIndexPage(
                    title="Portfolio",
                    slug="home",
                    intro='Welcome to my creative portfolio'
                )
                root.add_child(instance=portfolio_page)
                self.stdout.write(self.style.SUCCESS('Created Portfolio page'))
            else:
                self.stdout.write('Portfolio page already exists')
            
            # 3. Публикуем страницу
            portfolio_page.live = True
            portfolio_page.save()
            
            # 4. Устанавливаем как главную
            site = Site.objects.first()
            if site:
                site.root_page = portfolio_page
                site.save()
                self.stdout.write(self.style.SUCCESS('Set as home page'))
            
            self.stdout.write(self.style.SUCCESS('✅ DONE! Check your site now!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
