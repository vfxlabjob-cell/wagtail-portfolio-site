from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"
    
    def ready(self):
        # Создаем суперпользователя при запуске приложения
        import os
        from django.contrib.auth import get_user_model
        
        # Проверяем, что мы в продакшене
        if os.environ.get('DJANGO_SETTINGS_MODULE') == 'mysite.settings.production':
            User = get_user_model()
            username = 'admin'
            email = 'admin@example.com'
            password = 'admin123'
            
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email, password)
                print(f'✅ Superuser "{username}" created successfully!')