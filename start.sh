#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Change to the mysite directory
cd mysite

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
