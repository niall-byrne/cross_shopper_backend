"""Admin models for the stores app."""

from django.contrib import admin
from stores.admin.franchise import FranchiseAdmin
from stores.admin.store import StoreAdmin
from stores.models import Franchise, Store

admin.site.register(Franchise, FranchiseAdmin)
admin.site.register(Store, StoreAdmin)
