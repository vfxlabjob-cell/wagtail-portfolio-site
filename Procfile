release: cd mysite && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py force_create_superuser && python manage.py create_home && python manage.py create_site_content
web: cd mysite && python manage.py force_create_superuser && gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
