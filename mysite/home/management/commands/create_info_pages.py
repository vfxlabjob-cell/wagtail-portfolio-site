from django.core.management.base import BaseCommand
from wagtail.models import Page
from home.models import InfoIndexPage, InfoPage


class Command(BaseCommand):
    help = 'Create Information pages'

    def handle(self, *args, **options):
        self.stdout.write("=== CREATING INFORMATION PAGES ===")
        
        try:
            # 1. Находим корневую страницу
            root_page = Page.objects.filter(depth=1).first()
            if not root_page:
                self.stdout.write(self.style.ERROR('❌ Root page not found'))
                return
            
            # 2. Создаем InfoIndexPage если её нет
            info_index_page = InfoIndexPage.objects.filter(slug="information").first()
            if not info_index_page:
                info_index_page = InfoIndexPage(
                    title="Information",
                    slug="information",
                    intro="Welcome to our information section"
                )
                root_page.add_child(instance=info_index_page)
                info_index_page.live = True
                info_index_page.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Created InfoIndexPage: {info_index_page.title}'))
            else:
                self.stdout.write(f'InfoIndexPage already exists: {info_index_page.title}')
            
            # 3. Создаем стандартные Information страницы
            info_pages_data = [
                {
                    'title': 'Terms of Service',
                    'slug': 'terms-of-service',
                    'body': '<p>Terms of Service content goes here...</p>'
                },
                {
                    'title': 'Privacy Policy',
                    'slug': 'privacy-policy',
                    'body': '<p>Privacy Policy content goes here...</p>'
                },
                {
                    'title': 'About Us',
                    'slug': 'about-us',
                    'body': '<p>About Us content goes here...</p>'
                },
                {
                    'title': 'Contact',
                    'slug': 'contact',
                    'body': '<p>Contact information goes here...</p>'
                }
            ]
            
            for page_data in info_pages_data:
                existing_page = InfoPage.objects.filter(slug=page_data['slug']).first()
                if not existing_page:
                    info_page = InfoPage(
                        title=page_data['title'],
                        slug=page_data['slug'],
                        body=page_data['body']
                    )
                    info_index_page.add_child(instance=info_page)
                    info_page.live = True
                    info_page.save()
                    self.stdout.write(self.style.SUCCESS(f'✅ Created InfoPage: {info_page.title}'))
                else:
                    self.stdout.write(f'InfoPage already exists: {existing_page.title}')
            
            self.stdout.write(self.style.SUCCESS("=== INFORMATION PAGES CREATION COMPLETE ==="))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
            import traceback
            traceback.print_exc()
