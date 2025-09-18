#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Change to the mysite directory where manage.py is located
cd mysite

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput --settings=mysite.settings.production

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=mysite.settings.production

# Conditionally import data and fix the site root
if [ "$RUN_IMPORT" = "True" ]; then
    echo ">>> RUNNING DATA IMPORT"
    python manage.py import_site_data --settings=mysite.settings.production
    echo ">>> FIXING SITE ROOT"
    python manage.py fix_site_root --settings=mysite.settings.production
else
    echo ">>> SKIPPING DATA IMPORT"
fi

# Start the Gunicorn server for production
echo "Starting Gunicorn server..."
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
