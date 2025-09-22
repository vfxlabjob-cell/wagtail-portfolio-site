from django.core.management.base import BaseCommand
from wagtail.models import Site, Page
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Setup site for Railway deployment'

    def handle(self, *args, **options):
        self.stdout.write("=== Настройка для Railway ===")
        
        # Настраиваем Site
        try:
            site = Site.objects.first()
            if site:
                site.hostname = 'web-production-c60254.up.railway.app'
                site.port = 443
                site.is_default_site = True
                site.save()
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Site настроен: {site.hostname}:{site.port}")
                )
            else:
                # Создаем новый site
                root_page = Page.objects.get(id=1)
                site = Site.objects.create(
                    hostname='web-production-c60254.up.railway.app',
                    port=443,
                    root_page=root_page,
                    is_default_site=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Site создан: {site.hostname}:{site.port}")
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"✗ Ошибка настройки Site: {e}")
            )

        # Проверяем/создаем суперпользователя
        try:
            admin_user = User.objects.filter(username='admin').first()
            if admin_user:
                admin_user.is_superuser = True
                admin_user.is_staff = True
                admin_user.is_active = True
                admin_user.set_password('admin123')
                admin_user.save()
                self.stdout.write(
                    self.style.SUCCESS("✓ Пользователь admin обновлен")
                )
            else:
                User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
                self.stdout.write(
                    self.style.SUCCESS("✓ Создан новый суперпользователь admin")
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"✗ Ошибка настройки пользователя: {e}")
            )

        self.stdout.write(
            self.style.SUCCESS("=== Настройка завершена ===")
        )
