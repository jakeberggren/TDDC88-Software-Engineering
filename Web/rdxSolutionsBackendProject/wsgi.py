"""
WSGI config for rdxSolutionsBackendProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from pathlib import Path
import dotenv
from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent

CURRENT_DIR = Path(__file__).resolve().parent




if str(os.environ.get('DEBUG')) == "1" :
    ENV_FILE_PATH = BASE_DIR / ".env"
    dotenv.read_dotenv(str(ENV_FILE_PATH))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rdxSolutionsBackendProject.settings')

application = get_wsgi_application()

