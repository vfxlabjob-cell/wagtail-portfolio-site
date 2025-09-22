web: cd mysite && python manage.py migrate --settings=production && python manage.py collectstatic --noinput --settings=production && gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
