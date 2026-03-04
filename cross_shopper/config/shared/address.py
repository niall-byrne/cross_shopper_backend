"""Configuration for django-address."""

import os

GOOGLE_API_KEY = os.getenv("DJANGO_GOOGLE_MAPS_API_KEY", None)
