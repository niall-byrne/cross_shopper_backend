"""Admin for the store model."""

from django.contrib import admin
from stores.models import Store


class StoreAdmin(admin.ModelAdmin[Store]):
  ordering = ('franchise__name', 'franchise_location')
