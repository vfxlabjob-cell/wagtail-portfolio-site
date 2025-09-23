from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage, ProjectCategory

class Command(BaseCommand):
    help = 'Reset page structure to fix creation issues'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== RESETTING PAGE STRUCTURE ===")
            
            # 1. Удаляем все страницы кроме корневой
            root_page = Page.objects.filter(depth=1).first()
            if root_page:
                self.stdout.write(f'Found root page: {root_page.title}')
                
                # Удаляем все дочерние страницы
                children = root_page.get_children()
                for child in children:
                    self.stdout.write(f'Deleting child page: {child.title}')
                    child.delete()
            
            # 2. Создаем новую главную страницу
            portfolio_page = PortfolioIndexPage(
                title="Portfolio",
                slug="home",
                intro='Welcome to my creative portfolio'
            )
            root_page.add_child(instance=portfolio_page)
            portfolio_page.live = True
            portfolio_page.save()
            self.stdout.write(self.style.SUCCESS(f'Created new Portfolio page: {portfolio_page.title}'))
            
            # 3. Создаем категории
            categories_data = [
                {'name': 'Web Development', 'slug': 'web-development'},
                {'name': 'Mobile Apps', 'slug': 'mobile-apps'},
                {'name': 'Design', 'slug': 'design'},
            ]
            
            for cat_data in categories_data:
                category, created = ProjectCategory.objects.get_or_create(
                    slug=cat_data['slug'],
                    defaults={
                        'name': cat_data['name'],
                        'main_text': f'Projects in {cat_data["name"]}',
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
                else:
                    self.stdout.write(f'Category already exists: {category.name}')
            
            # 4. Обновляем настройки сайта
            site = Site.objects.first()
            if site:
                site.root_page = portfolio_page
                site.save()
                self.stdout.write(self.style.SUCCESS(f'Updated site root to: {portfolio_page.title}'))
            
            self.stdout.write(self.style.SUCCESS("\n=== PAGE STRUCTURE RESET COMPLETE ==="))
            self.stdout.write(f"Root page: {root_page.title}")
            self.stdout.write(f"Home page: {portfolio_page.title}")
            self.stdout.write(f"Categories: {ProjectCategory.objects.count()}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            import traceback
            traceback.print_exc()
