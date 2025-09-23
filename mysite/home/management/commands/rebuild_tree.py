from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage, ProjectCategory

class Command(BaseCommand):
    help = 'Rebuild the entire page tree structure'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== REBUILDING PAGE TREE ===")
            
            # 1. Находим корневую страницу
            root_page = Page.objects.filter(depth=1).first()
            if not root_page:
                self.stdout.write(self.style.ERROR("No root page found!"))
                return
            
            self.stdout.write(f'Found root page: {root_page.title}')
            
            # 2. Удаляем ВСЕ страницы кроме корневой
            all_pages = Page.objects.exclude(id=root_page.id)
            for page in all_pages:
                self.stdout.write(f'Deleting page: {page.title}')
                page.delete()
            
            # 3. Сбрасываем счетчики корневой страницы
            root_page.numchild = 0
            root_page.save()
            
            # 4. Создаем новую главную страницу с правильной структурой
            portfolio_page = PortfolioIndexPage(
                title="Portfolio",
                slug="home",
                intro='Welcome to my creative portfolio'
            )
            
            # Добавляем как дочернюю страницу (это правильно обновит дерево)
            root_page.add_child(instance=portfolio_page)
            portfolio_page.live = True
            portfolio_page.save()
            
            self.stdout.write(self.style.SUCCESS(f'Created Portfolio page: {portfolio_page.title}'))
            self.stdout.write(f'Portfolio page path: {portfolio_page.path}')
            self.stdout.write(f'Portfolio page depth: {portfolio_page.depth}')
            
            # 5. Создаем категории
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
            
            # 6. Обновляем настройки сайта
            site = Site.objects.first()
            if site:
                site.root_page = portfolio_page
                site.save()
                self.stdout.write(self.style.SUCCESS(f'Updated site root to: {portfolio_page.title}'))
            
            # 7. Проверяем структуру дерева
            self.stdout.write("\n=== TREE STRUCTURE ===")
            root_page.refresh_from_db()
            self.stdout.write(f'Root page numchild: {root_page.numchild}')
            
            children = root_page.get_children()
            for child in children:
                self.stdout.write(f'Child: {child.title} (path: {child.path}, depth: {child.depth})')
            
            self.stdout.write(self.style.SUCCESS("\n=== TREE REBUILD COMPLETE ==="))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            import traceback
            traceback.print_exc()
