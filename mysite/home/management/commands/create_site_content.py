from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage, ProjectCategory, ProjectPage, InfoIndexPage, InfoPage
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create initial site content for Railway deployment'

    def handle(self, *args, **options):
        try:
            self.stdout.write("=== CREATING SITE CONTENT ===")
            
            # 1. Создаем корневую страницу Portfolio
            root_page = Page.objects.filter(depth=1).first()
            if not root_page:
                self.stdout.write(self.style.ERROR("No root page found!"))
                return
            
            # 2. Создаем PortfolioIndexPage если не существует
            portfolio_page = PortfolioIndexPage.objects.filter(slug="home").first()
            if not portfolio_page:
                portfolio_page = PortfolioIndexPage(
                    title="Home",
                    slug="home",
                    intro='Welcome to my portfolio'
                )
                root_page.add_child(instance=portfolio_page)
                self.stdout.write(self.style.SUCCESS(f'Created Home page: {portfolio_page.title}'))
            else:
                self.stdout.write(f'Home page already exists: {portfolio_page.title}')
            
            # 3. Создаем категории проектов
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
            
            # 4. Создаем примеры проектов
            projects_data = [
                {
                    'title': 'E-commerce Website',
                    'slug': 'ecommerce-website',
                    'category': 'web-development',
                    'intro': 'Modern e-commerce platform with React and Django',
                },
                {
                    'title': 'Mobile Banking App',
                    'slug': 'mobile-banking-app',
                    'category': 'mobile-apps',
                    'intro': 'Secure mobile banking application for iOS and Android',
                },
                {
                    'title': 'Brand Identity Design',
                    'slug': 'brand-identity-design',
                    'category': 'design',
                    'intro': 'Complete brand identity for tech startup',
                },
            ]
            
            for proj_data in projects_data:
                try:
                    category = ProjectCategory.objects.get(slug=proj_data['category'])
                    project, created = ProjectPage.objects.get_or_create(
                        slug=proj_data['slug'],
                        defaults={
                            'title': proj_data['title'],
                            'intro': proj_data['intro'],
                            'category': category,
                            'live': True,
                        }
                    )
                    if created:
                        # Устанавливаем правильный путь
                        project.path = portfolio_page.path + '0001'
                        project.depth = 3
                        project.save()
                        self.stdout.write(self.style.SUCCESS(f'Created project: {project.title}'))
                    else:
                        self.stdout.write(f'Project already exists: {project.title}')
                except ProjectCategory.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Category not found: {proj_data["category"]}'))
            
            # 5. Создаем InfoIndexPage
            info_page, created = InfoIndexPage.objects.get_or_create(
                title="About",
                slug="about",
                defaults={
                    'intro': 'Learn more about me',
                    'live': True,
                }
            )
            if created:
                info_page.path = root_page.path + '0002'
                info_page.depth = 2
                info_page.save()
                self.stdout.write(self.style.SUCCESS(f'Created About page: {info_page.title}'))
            else:
                self.stdout.write(f'About page already exists: {info_page.title}')
            
            # 6. Создаем InfoPage
            info_detail, created = InfoPage.objects.get_or_create(
                title="About Me",
                slug="about-me",
                defaults={
                    'live': True,
                }
            )
            if created:
                info_detail.path = info_page.path + '0001'
                info_detail.depth = 3
                info_detail.save()
                self.stdout.write(self.style.SUCCESS(f'Created About Me page: {info_detail.title}'))
            else:
                self.stdout.write(f'About Me page already exists: {info_detail.title}')
            
            # 7. Убеждаемся, что все страницы опубликованы
            unpublished_pages = Page.objects.filter(live=False)
            for page in unpublished_pages:
                page.live = True
                page.save()
                self.stdout.write(self.style.SUCCESS(f'Published page: {page.title}'))
            
            # 8. Создаем или обновляем Site
            site, created = Site.objects.get_or_create(
                is_default_site=True,
                defaults={
                    'hostname': 'localhost',
                    'port': 8000,
                    'root_page': portfolio_page,
                }
            )
            if not created:
                site.root_page = portfolio_page
                site.save()
                self.stdout.write(self.style.SUCCESS('Updated default site'))
            else:
                self.stdout.write(self.style.SUCCESS('Created default site'))
            
            self.stdout.write(self.style.SUCCESS("\n=== CONTENT CREATION COMPLETE ==="))
            self.stdout.write(f"Total pages: {Page.objects.count()}")
            self.stdout.write(f"Portfolio pages: {PortfolioIndexPage.objects.count()}")
            self.stdout.write(f"Categories: {ProjectCategory.objects.count()}")
            self.stdout.write(f"Projects: {ProjectPage.objects.count()}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating content: {e}')
            )
