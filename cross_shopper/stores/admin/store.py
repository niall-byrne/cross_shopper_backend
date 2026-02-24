"""Admin for the store model."""

from django.contrib import admin
from stores.models import Store

from . import filters


class StoreAdmin(admin.ModelAdmin[Store]):
  list_filter = filters.store_filter
  ordering = ('franchise__name', 'franchise_location')
