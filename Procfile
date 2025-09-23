release: cd mysite && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py rebuild_tree
web: cd mysite && gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
