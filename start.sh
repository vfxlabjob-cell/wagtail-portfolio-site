#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting deployment process..."

# Change to the mysite directory where manage.py is located
cd mysite

# Check if we can connect to the database
echo "Checking database connection..."
python manage.py check --database default --settings=mysite.settings.production

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput --settings=mysite.settings.production

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=mysite.settings.production

# Create superuser if it doesn't exist (optional - only if DJANGO_SUPERUSER_* env vars are set)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py shell --settings=mysite.settings.production -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"
fi

# Start the Gunicorn server for production
echo "Starting Gunicorn server on port $PORT..."
DJANGO_SETTINGS_MODULE=mysite.settings.production exec gunicorn mysite.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info
