"""Production environment specific configuration."""

from pathlib import Path
from typing import List

from .shared import *  # noqa: F403

ENVIRONMENT = 'PRODUCTION'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS: List[str] = ["127.0.0.1", "localhost"]

# Cache
# https://docs.djangoproject.com/en/4.2/ref/settings/#caches

CACHES = {
    'default':
        {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'TIMEOUT': 60,
            'OPTIONS': {
                'MAX_ENTRIES': 10000
            }
        }
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "db.production.sqlite",
        }
}
