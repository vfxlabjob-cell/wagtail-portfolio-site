from django.core.management.base import BaseCommand
from wagtail.models import Page
from home.models import ProjectCategory

class Command(BaseCommand):
    help = 'Fix page creation issues'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== FIXING PAGE CREATION ===")
            
            # 1. Убеждаемся, что есть категории
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
            
            # 2. Проверяем структуру страниц
            root_page = Page.objects.filter(depth=1).first()
            if root_page:
                self.stdout.write(f'Root page: {root_page.title}')
                
                # Проверяем дочерние страницы
                children = root_page.get_children()
                for child in children:
                    self.stdout.write(f'Child page: {child.title} (depth: {child.depth})')
            
            self.stdout.write(self.style.SUCCESS("\n=== PAGE FIX COMPLETE ==="))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            import traceback
            traceback.print_exc()
