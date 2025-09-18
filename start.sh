#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Change to the mysite directory
cd mysite

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput --settings=mysite.settings.no_csrf

# Create superuser if not exists
echo "Creating superuser..."
python manage.py create_superuser --settings=mysite.settings.no_csrf

# Clear corrupted sessions
echo "Clearing corrupted sessions..."
python manage.py clear_sessions --settings=mysite.settings.no_csrf

# Diagnose site
echo "Diagnosing site..."
python manage.py diagnose_site --settings=mysite.settings.no_csrf

# Import real site data
echo "Importing real site data..."
python manage.py import_site_data --settings=mysite.settings.no_csrf

# Publish existing pages
echo "Publishing existing pages..."
python manage.py publish_pages --settings=mysite.settings.no_csrf

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=mysite.settings.no_csrf

# Start the Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --settings=mysite.settings.no_csrf
