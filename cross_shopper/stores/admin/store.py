"""Admin for the store model."""

from django.contrib import admin
from stores.admin.list_filters.store import store_list_filter
from stores.models import Store


class StoreAdmin(admin.ModelAdmin[Store]):
  list_filter = store_list_filter
  ordering = ("franchise__name", "franchise_location")
