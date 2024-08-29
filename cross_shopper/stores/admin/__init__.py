"""Admin models for the stores app."""

from django.contrib import admin
from stores.models import Franchise, Store

admin.site.register(Franchise)
admin.site.register(Store)
