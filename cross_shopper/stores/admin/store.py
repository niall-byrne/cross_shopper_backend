"""Admin for the store model."""

from django.contrib import admin
from stores.admin import filters
from stores.models import Store


class StoreAdmin(admin.ModelAdmin[Store]):
  list_filter = filters.store_filter
  ordering = ('franchise__name', 'franchise_location')
