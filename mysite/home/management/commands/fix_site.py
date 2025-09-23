from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage, ProjectCategory


class Command(BaseCommand):
    help = 'Fix site structure and create missing pages'

    def handle(self, *args, **options):
        self.stdout.write("=== FIXING SITE STRUCTURE ===")
        
        # 1. Создаем суперпользователя
        User = get_user_model()
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'✅ Superuser "{username}" created successfully!'))
        else:
            self.stdout.write(f'Superuser "{username}" already exists')
        
        # 2. Проверяем и исправляем структуру страниц
        root_page = Page.objects.filter(depth=1).first()
        if root_page:
            # Проверяем, есть ли уже Portfolio страница
            portfolio_page = PortfolioIndexPage.objects.filter(slug="home").first()
            
            if not portfolio_page:
                # Создаем новую главную страницу только если её нет
                portfolio_page = PortfolioIndexPage(
                    title="Portfolio",
                    slug="home",
                    intro='Welcome to my creative portfolio'
                )
                
                root_page.add_child(instance=portfolio_page)
                portfolio_page.live = True
                portfolio_page.save()
                
                self.stdout.write(self.style.SUCCESS(f'✅ Created Portfolio page: {portfolio_page.title}'))
            else:
                self.stdout.write(f'Portfolio page already exists: {portfolio_page.title}')
            
            # Обновляем счетчики корневой страницы
            root_page.numchild = Page.objects.filter(parent=root_page).count()
            root_page.save()
        
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
                self.stdout.write(self.style.SUCCESS(f'✅ Created category: {category.name}'))
            else:
                self.stdout.write(f'Category already exists: {category.name}')
        
        # 4. Настраиваем Site объект
        if portfolio_page:
            # Удаляем все существующие сайты
            Site.objects.all().delete()
            self.stdout.write('🗑️ Deleted all existing sites')
            
            # Создаем новый сайт
            site = Site.objects.create(
                hostname='web-production-b4d2a.up.railway.app',
                port=443,
                root_page=portfolio_page,
                is_default_site=True,
                site_name='Portfolio Site'
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Created new site: {site.site_name}'))
            self.stdout.write(f'   Hostname: {site.hostname}')
            self.stdout.write(f'   Root page: {site.root_page.title}')
            self.stdout.write(f'   Is default: {site.is_default_site}')
        
        self.stdout.write(self.style.SUCCESS("=== SITE FIX COMPLETE ==="))
