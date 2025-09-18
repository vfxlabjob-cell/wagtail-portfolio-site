from django.core.management.base import BaseCommand
from wagtail.models import Page
from home.models import PortfolioIndexPage, ProjectCategory, ProjectPage

class Command(BaseCommand):
    help = 'Publish all pages that are not live'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== PUBLISHING PAGES ===")
            
            # Публикуем все страницы, которые не live
            unpublished_pages = Page.objects.filter(live=False)
            self.stdout.write(f"Found {unpublished_pages.count()} unpublished pages")
            
            for page in unpublished_pages:
                try:
                    page.live = True
                    page.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Published: {page.title} (ID: {page.id})')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error publishing {page.title}: {e}')
                    )
            
            # Специально для PortfolioIndexPage
            portfolio_pages = PortfolioIndexPage.objects.filter(live=False)
            for page in portfolio_pages:
                try:
                    page.live = True
                    page.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Published Portfolio: {page.title}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error publishing Portfolio {page.title}: {e}')
                    )
            
            # Специально для ProjectCategory
            categories = ProjectCategory.objects.filter(live=False)
            for cat in categories:
                try:
                    cat.live = True
                    cat.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Published Category: {cat.name}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error publishing Category {cat.name}: {e}')
                    )
            
            # Специально для ProjectPage
            projects = ProjectPage.objects.filter(live=False)
            for project in projects:
                try:
                    project.live = True
                    project.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Published Project: {project.title}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error publishing Project {project.title}: {e}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS('Publishing completed!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error publishing pages: {e}')
            )
