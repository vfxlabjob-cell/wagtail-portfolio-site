import os
from django.contrib.auth import get_user_model
from wagtail.models import Page, Site
from home.models import PortfolioIndexPage, ProjectCategory

class InitializationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.initialized = False

    def __call__(self, request):
        if not self.initialized and os.environ.get('DJANGO_SETTINGS_MODULE') == 'mysite.settings.production':
            self.initialize_site()
            self.initialized = True

        response = self.get_response(request)
        return response

    def initialize_site(self):
        try:
            print("=== INITIALIZING SITE ===")
            
            # 1. Создаем суперпользователя
            User = get_user_model()
            username = 'admin'
            email = 'admin@example.com'
            password = 'admin123'
            
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email, password)
                print(f'✅ Superuser "{username}" created successfully!')
            else:
                print(f'Superuser "{username}" already exists')
            
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
                    
                    print(f'✅ Created Portfolio page: {portfolio_page.title}')
                else:
                    print(f'Portfolio page already exists: {portfolio_page.title}')
                
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
                    print(f'✅ Created category: {category.name}')
                else:
                    print(f'Category already exists: {category.name}')
            
            # 4. Настраиваем Site объект
            if portfolio_page:
                site, created = Site.objects.get_or_create(
                    is_default_site=True,
                    defaults={
                        'hostname': 'web-production-b4d2a.up.railway.app',
                        'port': 443,
                        'root_page': portfolio_page,
                    }
                )
                if not created:
                    site.hostname = 'web-production-b4d2a.up.railway.app'
                    site.port = 443
                    site.root_page = portfolio_page
                    site.save()
                    print('✅ Updated default site')
                else:
                    print('✅ Created default site')
            
            print("=== SITE INITIALIZATION COMPLETE ===")
            
        except Exception as e:
            print(f'Error during initialization: {str(e)}')
            import traceback
            traceback.print_exc()
