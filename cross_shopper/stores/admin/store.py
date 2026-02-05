"""Admin for the store model."""

from django.contrib import admin
from stores.admin.filters.store import store_filter
from stores.models import Store


class StoreAdmin(admin.ModelAdmin[Store]):
  list_filter = store_filter
  ordering = ('franchise__name', 'franchise_location')
