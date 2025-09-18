web: cd mysite && python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
