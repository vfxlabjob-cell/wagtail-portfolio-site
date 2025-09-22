release: cd mysite && python manage.py migrate
web: cd mysite && gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
