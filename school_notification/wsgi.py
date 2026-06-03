"""
WSGI config for school_notification project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_notification.settings')

application = get_wsgi_application()
