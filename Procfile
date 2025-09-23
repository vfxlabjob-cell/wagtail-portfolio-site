release: cd mysite && python manage.py migrate && python manage.py collectstatic --noinput
web: cd mysite && python manage.py create_site && gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
