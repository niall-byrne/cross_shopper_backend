"""Admin models for the stores app."""

from django.contrib import admin
from stores.models import Franchise, Store
from .franchise import FranchiseAdmin
from .store import StoreAdmin

admin.site.register(Franchise, FranchiseAdmin)
admin.site.register(Store, StoreAdmin)
