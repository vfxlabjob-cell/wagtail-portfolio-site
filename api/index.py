import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Add mysite directory to path
mysite_path = os.path.join(project_root, 'mysite')
sys.path.insert(0, mysite_path)

# Add mysite/mysite directory to path (for settings)
mysite_settings_path = os.path.join(mysite_path, 'mysite')
sys.path.insert(0, mysite_settings_path)

# Debug: Print paths
print(f"Project root: {project_root}")
print(f"Mysite path: {mysite_path}")
print(f"Mysite settings path: {mysite_settings_path}")
print(f"Python path: {sys.path}")

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.production')

# Get WSGI application
application = get_wsgi_application()

# Vercel handler
def handler(request):
    return application(request)

# Для совместимости с Vercel
app = application
