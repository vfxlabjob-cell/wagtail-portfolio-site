from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from wagtail.models import Page, Site
from wagtail.models import Locale
from home.models import PortfolioIndexPage, InfoIndexPage
import os


class Command(BaseCommand):
    help = 'Initialize the site with superuser and pages'

    def handle(self, *args, **options):
        self.stdout.write('Starting site initialization...')
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            password = os.environ.get('ADMIN_PASSWORD', 'admin123')
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS('Superuser "admin" created successfully')
            )
        else:
            self.stdout.write('Superuser "admin" already exists')
        
        # Create root page if it doesn't exist
        root = Page.objects.filter(depth=1).first()
        if not root:
            root = Page.objects.create(
                title="Root",
                slug="root",
                content_type=Page._meta.get_field('content_type').default,
                path="0001",
                depth=1,
                numchild=0,
                url_path="/",
            )
            self.stdout.write('Root page created')
        
        # Create portfolio index page if it doesn't exist
        portfolio_page = PortfolioIndexPage.objects.filter(slug='portfolio').first()
        if not portfolio_page:
            portfolio_page = PortfolioIndexPage(
                title="Portfolio",
                slug="portfolio",
                intro="Welcome to our portfolio",
                show_in_menus=True,
            )
            root.add_child(instance=portfolio_page)
            self.stdout.write('Portfolio index page created')
        
        # Create info index page if it doesn't exist
        info_page = InfoIndexPage.objects.filter(slug='info').first()
        if not info_page:
            info_page = InfoIndexPage(
                title="Information",
                slug="info",
                intro="Information pages",
                show_in_menus=True,
            )
            root.add_child(instance=info_page)
            self.stdout.write('Info index page created')
        
        # Create or update site
        site = Site.objects.first()
        if not site:
            # Get the default locale
            locale = Locale.objects.first()
            if not locale:
                locale = Locale.objects.create(language_code='en')
            
            site = Site.objects.create(
                hostname='localhost',
                port=8000,
                root_page=portfolio_page,
                is_default_site=True,
                locale=locale,
            )
            self.stdout.write('Default site created')
        else:
            # Update root page if needed
            if site.root_page != portfolio_page:
                site.root_page = portfolio_page
                site.save()
                self.stdout.write('Site root page updated')
        
        self.stdout.write(
            self.style.SUCCESS('Site initialization completed successfully!')
        )
        self.stdout.write('You can now access:')
        self.stdout.write('- Admin panel: /admin/')
        self.stdout.write('- Portfolio: /portfolio/')
        self.stdout.write('- Info pages: /info/')
