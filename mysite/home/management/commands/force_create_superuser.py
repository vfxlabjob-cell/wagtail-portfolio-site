from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Force create a superuser'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'
        
        # Удаляем существующего пользователя если есть
        User.objects.filter(username=username).delete()
        
        # Создаем нового суперпользователя
        User.objects.create_superuser(username, email, password)
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created superuser "{username}" with password "{password}"')
        )
