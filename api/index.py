import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Also add mysite directory to path
mysite_path = os.path.join(project_root, 'mysite')
sys.path.insert(0, mysite_path)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.production')

# Get WSGI application
application = get_wsgi_application()

# Vercel handler
def handler(request):
    return application(request)
