from django.core.management.base import BaseCommand
from wagtail.models import Page
from home.models import PortfolioIndexPage, ProjectCategory, ProjectPage

class Command(BaseCommand):
    help = 'List all existing pages in the site'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== EXISTING PAGES ===")
            
            # Показываем все страницы
            pages = Page.objects.all().order_by('path')
            for page in pages:
                self.stdout.write(f"ID: {page.id}, Title: {page.title}, Type: {page.__class__.__name__}, Live: {page.live}")
            
            self.stdout.write("\n=== PORTFOLIO PAGES ===")
            portfolio_pages = PortfolioIndexPage.objects.all()
            for page in portfolio_pages:
                self.stdout.write(f"Portfolio: {page.title} (Live: {page.live})")
            
            self.stdout.write("\n=== PROJECT CATEGORIES ===")
            categories = ProjectCategory.objects.all()
            for cat in categories:
                self.stdout.write(f"Category: {cat.name} (Live: {cat.live})")
            
            self.stdout.write("\n=== PROJECT PAGES ===")
            projects = ProjectPage.objects.all()
            for project in projects:
                self.stdout.write(f"Project: {project.title} (Live: {project.live})")
            
            self.stdout.write("\n=== SUMMARY ===")
            self.stdout.write(f"Total pages: {Page.objects.count()}")
            self.stdout.write(f"Portfolio pages: {portfolio_pages.count()}")
            self.stdout.write(f"Categories: {categories.count()}")
            self.stdout.write(f"Projects: {projects.count()}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error listing pages: {e}')
            )
