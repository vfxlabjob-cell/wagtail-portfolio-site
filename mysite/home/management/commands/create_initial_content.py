from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from home.models import PortfolioIndexPage, ProjectCategory, ProjectPage
from wagtail.core.models import Site, Page
from wagtail.images.models import Image
import os

class Command(BaseCommand):
    help = 'Create initial content for the site'

    def handle(self, *args, **options):
        try:
            # Получаем корневую страницу
            root_page = Page.objects.get(depth=1)
            
            # Создаем главную страницу портфолио, если её нет
            portfolio_page, created = PortfolioIndexPage.objects.get_or_create(
                title="Portfolio",
                slug="portfolio",
                defaults={
                    'intro': 'Welcome to my portfolio',
                    'live': True,
                }
            )
            
            if created:
                # Добавляем как дочернюю страницу корневой
                portfolio_page.move(root_page, pos='last-child')
                self.stdout.write(
                    self.style.SUCCESS('Created Portfolio page')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('Portfolio page already exists')
                )
            
            # Создаем категории проектов
            categories_data = [
                {'name': 'Web Development', 'slug': 'web-development'},
                {'name': 'Mobile Apps', 'slug': 'mobile-apps'},
                {'name': 'Design', 'slug': 'design'},
            ]
            
            for cat_data in categories_data:
                category, created = ProjectCategory.objects.get_or_create(
                    name=cat_data['name'],
                    slug=cat_data['slug'],
                    defaults={
                        'main_text': f'Projects in {cat_data["name"]}',
                        'live': True,
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created category: {cat_data["name"]}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Category already exists: {cat_data["name"]}')
                    )
            
            # Создаем примеры проектов
            projects_data = [
                {
                    'title': 'Sample Web Project',
                    'slug': 'sample-web-project',
                    'category': 'Web Development',
                    'description': 'This is a sample web development project',
                },
                {
                    'title': 'Sample Mobile App',
                    'slug': 'sample-mobile-app',
                    'category': 'Mobile Apps',
                    'description': 'This is a sample mobile application',
                },
            ]
            
            for project_data in projects_data:
                try:
                    category = ProjectCategory.objects.get(name=project_data['category'])
                    
                    project, created = ProjectPage.objects.get_or_create(
                        title=project_data['title'],
                        slug=project_data['slug'],
                        defaults={
                            'description': project_data['description'],
                            'category': category,
                            'live': True,
                        }
                    )
                    
                    if created:
                        # Добавляем как дочернюю страницу портфолио
                        project.move(portfolio_page, pos='last-child')
                        self.stdout.write(
                            self.style.SUCCESS(f'Created project: {project_data["title"]}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Project already exists: {project_data["title"]}')
                        )
                        
                except ProjectCategory.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'Category not found: {project_data["category"]}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS('Initial content created successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating initial content: {e}')
            )
