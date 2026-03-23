import os

from django.core.wsgi import get_wsgi_application

# We tell Django to use the settings file inside your specific folder
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freedom.settings')

application = get_wsgi_application()