from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage, ProjectCategory


class Command(BaseCommand):
    help = 'Check current site structure and settings'

    def handle(self, *args, **options):
        self.stdout.write("=== CHECKING SITE STRUCTURE ===")
        
        # 1. Проверяем суперпользователя
        User = get_user_model()
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            self.stdout.write(f'✅ Superuser exists: {admin_user.username}')
        else:
            self.stdout.write(self.style.ERROR('❌ Superuser does not exist'))
        
        # 2. Проверяем структуру страниц
        root_page = Page.objects.filter(depth=1).first()
        if root_page:
            self.stdout.write(f'✅ Root page exists: {root_page.title}')
            self.stdout.write(f'   Children count: {root_page.numchild}')
            
            # Проверяем Portfolio страницу
            portfolio_page = PortfolioIndexPage.objects.filter(slug="home").first()
            if portfolio_page:
                self.stdout.write(f'✅ Portfolio page exists: {portfolio_page.title}')
                self.stdout.write(f'   Slug: {portfolio_page.slug}')
                self.stdout.write(f'   Live: {portfolio_page.live}')
                self.stdout.write(f'   Parent: {portfolio_page.get_parent().title if portfolio_page.get_parent() else "None"}')
            else:
                self.stdout.write(self.style.ERROR('❌ Portfolio page does not exist'))
        else:
            self.stdout.write(self.style.ERROR('❌ Root page does not exist'))
        
        # 3. Проверяем категории
        categories = ProjectCategory.objects.all()
        self.stdout.write(f'✅ Categories count: {categories.count()}')
        for category in categories:
            self.stdout.write(f'   - {category.name} ({category.slug})')
        
        # 4. Проверяем Site объекты
        sites = Site.objects.all()
        self.stdout.write(f'✅ Sites count: {sites.count()}')
        for site in sites:
            self.stdout.write(f'   - {site.site_name or "Unnamed"}')
            self.stdout.write(f'     Hostname: {site.hostname}')
            self.stdout.write(f'     Port: {site.port}')
            self.stdout.write(f'     Root page: {site.root_page.title if site.root_page else "None"}')
            self.stdout.write(f'     Is default: {site.is_default_site}')
        
        # 5. Проверяем все страницы
        all_pages = Page.objects.all()
        self.stdout.write(f'✅ Total pages: {all_pages.count()}')
        for page in all_pages:
            self.stdout.write(f'   - {page.title} (depth: {page.depth}, live: {page.live})')
        
        self.stdout.write("=== SITE CHECK COMPLETE ===")
