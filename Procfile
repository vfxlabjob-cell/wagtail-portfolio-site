release: cd mysite && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py create_superuser && python manage.py create_home && python manage.py create_site_content
web: cd mysite && gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
