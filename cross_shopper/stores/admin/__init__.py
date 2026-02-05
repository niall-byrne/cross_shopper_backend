"""Admin models for the stores app."""

from django.contrib import admin
from stores.models import Franchise, Store
from . import filters
from .franchise import FranchiseAdmin
from .store import StoreAdmin

admin.site.register(
    Franchise, FranchiseAdmin, list_filter=filters.franchise_filter
)
admin.site.register(Store, StoreAdmin, list_filter=filters.store_filter)
