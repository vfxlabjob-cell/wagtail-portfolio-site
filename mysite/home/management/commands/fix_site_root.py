from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

class Command(BaseCommand):
    help = 'Sets the root page of the default site to the page titled "Potrfolio Site"'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=== FIXING SITE ROOT PAGE ==="))

        try:
            # Ищем страницу портфолио. Убедитесь, что название точное.
            # В вашем экспорте было "Potrfolio Site", возможно, с опечаткой.
            # Пробуем найти и с опечаткой, и с правильным написанием.
            portfolio_page = None
            possible_titles = ["Potrfolio Site", "Portfolio Site", "Portfolio"]
            for title in possible_titles:
                portfolio_page = Page.objects.filter(title=title).first()
                if portfolio_page:
                    self.stdout.write(f"Found page: '{title}' (ID: {portfolio_page.id})")
                    break
            
            if not portfolio_page:
                self.stdout.write(self.style.ERROR("Could not find a page with title 'Potrfolio Site', 'Portfolio Site', or 'Portfolio'."))
                self.stdout.write(self.style.WARNING("Please check the title of your main page."))
                # Попробуем взять первую страницу, которая не является "Root" или "Home"
                fallback_page = Page.objects.exclude(title__in=["Root", "Home"]).order_by('path').first()
                if fallback_page:
                    self.stdout.write(f"Using fallback page: '{fallback_page.title}' (ID: {fallback_page.id})")
                    portfolio_page = fallback_page
                else:
                    return

            # Ищем сайт по умолчанию
            default_site = Site.objects.filter(is_default_site=True).first()

            if not default_site:
                self.stdout.write(self.style.ERROR("No default site found."))
                # Создаем сайт, если его нет
                self.stdout.write("Creating a new default site...")
                root = Page.objects.get(depth=1)
                default_site = Site.objects.create(
                    hostname='localhost', 
                    root_page=root, 
                    is_default_site=True,
                    site_name='My Site'
                )
                self.stdout.write(f"Created new default site for hostname: {default_site.hostname}")

            if default_site.root_page.id == portfolio_page.id:
                self.stdout.write(self.style.SUCCESS(f"Default site root page is already correctly set to '{portfolio_page.title}'."))
            else:
                self.stdout.write(f"Current root page is: '{default_site.root_page.title}' (ID: {default_site.root_page.id})")
                self.stdout.write(f"Setting new root page to: '{portfolio_page.title}' (ID: {portfolio_page.id})")
                default_site.root_page = portfolio_page
                default_site.save()
                self.stdout.write(self.style.SUCCESS("Successfully updated the default site's root page!"))

        except Page.DoesNotExist:
            self.stdout.write(self.style.ERROR("The page 'Potrfolio Site' does not exist in the database."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
