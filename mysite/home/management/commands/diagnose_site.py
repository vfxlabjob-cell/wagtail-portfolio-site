from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage, ProjectCategory, ProjectPage, InfoIndexPage, InfoPage
from django.contrib.sessions.models import Session

class Command(BaseCommand):
    help = 'Diagnose site issues'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== SITE DIAGNOSIS ===")
            
            # Проверяем корневую страницу
            root_pages = Page.objects.filter(depth=1)
            self.stdout.write(f"Root pages: {root_pages.count()}")
            for page in root_pages:
                self.stdout.write(f"  - {page.title} (ID: {page.id}, Live: {page.live})")
            
            # Проверяем все страницы
            all_pages = Page.objects.all().order_by('path')
            self.stdout.write(f"\nAll pages: {all_pages.count()}")
            for page in all_pages:
                self.stdout.write(f"  - {page.title} (ID: {page.id}, Live: {page.live}, Path: {page.path})")
            
            # Проверяем сайты
            sites = Site.objects.all()
            self.stdout.write(f"\nSites: {sites.count()}")
            for site in sites:
                self.stdout.write(f"  - {site.hostname} (Root: {site.root_page.title if site.root_page else 'None'})")
            
            # Проверяем сессии
            sessions = Session.objects.all()
            self.stdout.write(f"\nSessions: {sessions.count()}")
            
            # Проверяем категории
            categories = ProjectCategory.objects.all()
            self.stdout.write(f"\nCategories: {categories.count()}")
            for cat in categories:
                self.stdout.write(f"  - {cat.name} (Live: {cat.live})")
            
            # Проверяем проекты
            projects = ProjectPage.objects.all()
            self.stdout.write(f"\nProjects: {projects.count()}")
            for project in projects:
                self.stdout.write(f"  - {project.title} (Live: {project.live})")
            
            self.stdout.write("\n=== DIAGNOSIS COMPLETE ===")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during diagnosis: {e}')
            )
