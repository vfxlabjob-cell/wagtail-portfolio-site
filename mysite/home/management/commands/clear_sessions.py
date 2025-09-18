from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone

class Command(BaseCommand):
    help = 'Clear all corrupted sessions from database'

    def handle(self, *args, **options):
        try:
            # Удаляем все сессии
            deleted_count = Session.objects.all().delete()[0]
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {deleted_count} sessions')
            )
            
            # Очищаем устаревшие сессии
            expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
            expired_count = expired_sessions.delete()[0]
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {expired_count} expired sessions')
            )
            
            self.stdout.write(
                self.style.SUCCESS('All sessions cleared successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error clearing sessions: {e}')
            )
