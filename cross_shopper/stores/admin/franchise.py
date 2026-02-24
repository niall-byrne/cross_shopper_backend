"""Admin for the franchise model."""

from django.contrib import admin
from stores.admin.list_filter.franchise import franchise_filter
from stores.models import Franchise


class FranchiseAdmin(admin.ModelAdmin[Franchise]):
  list_filter = franchise_filter
  ordering = ('name',)
