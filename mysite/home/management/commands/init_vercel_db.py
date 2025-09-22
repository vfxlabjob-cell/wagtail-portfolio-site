from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from wagtail.models import Site
from home.models import PortfolioIndexPage, CardsIndexPage
from wagtail.images.models import Image
import os

class Command(BaseCommand):
    help = 'Initialize Vercel database with basic structure'

    def handle(self, *args, **options):
        self.stdout.write("=== INITIALIZING VERCEL DATABASE ===")
        
        try:
            # 1. Run migrations
            self.stdout.write("Running migrations...")
            call_command('migrate', verbosity=0)
            self.stdout.write("✓ Migrations completed")
            
            # 2. Create superuser if not exists
            self.stdout.write("Creating superuser...")
            from django.contrib.auth.models import User
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'
                )
                self.stdout.write("✓ Superuser created (admin/admin123)")
            else:
                self.stdout.write("✓ Superuser already exists")
            
            # 3. Create default site
            self.stdout.write("Setting up default site...")
            site, created = Site.objects.get_or_create(
                is_default_site=True,
                defaults={
                    'hostname': 'localhost',
                    'port': 8000,
                    'site_name': 'Portfolio Site',
                }
            )
            if created:
                self.stdout.write("✓ Default site created")
            else:
                self.stdout.write("✓ Default site already exists")
            
            # 4. Create root page
            self.stdout.write("Creating root page...")
            root_page = PortfolioIndexPage.objects.filter(slug='').first()
            if not root_page:
                root_page = PortfolioIndexPage(
                    title='Portfolio',
                    slug='',
                    content_type_id=1,  # Page content type
                )
                root_page.save()
                self.stdout.write("✓ Root page created")
            else:
                self.stdout.write("✓ Root page already exists")
            
            # 5. Set site root page
            site.root_page = root_page
            site.save()
            self.stdout.write("✓ Site root page set")
            
            # 6. Create cards index page
            self.stdout.write("Creating cards index page...")
            cards_page = CardsIndexPage.objects.filter(slug='cards').first()
            if not cards_page:
                cards_page = CardsIndexPage(
                    title='Cards',
                    slug='cards',
                    content_type_id=1,
                )
                root_page.add_child(instance=cards_page)
                self.stdout.write("✓ Cards index page created")
            else:
                self.stdout.write("✓ Cards index page already exists")
            
            # 7. Import initial data
            self.stdout.write("Importing initial data...")
            call_command('simple_import', verbosity=0)
            self.stdout.write("✓ Initial data imported")
            
            self.stdout.write("\n=== VERCEL DATABASE INITIALIZED SUCCESSFULLY ===")
            self.stdout.write("You can now access:")
            self.stdout.write("- Admin: /admin/ (admin/admin123)")
            self.stdout.write("- Site: /")
            
        except Exception as e:
            self.stdout.write(f"Error: {e}")
            import traceback
            self.stdout.write(traceback.format_exc())
