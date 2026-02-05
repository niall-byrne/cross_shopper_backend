"""Admin for the franchise model."""

from django.contrib import admin
from stores.admin.list_filters.franchise import franchise_list_filter
from stores.models import Franchise


class FranchiseAdmin(admin.ModelAdmin[Franchise]):
  list_filter = franchise_list_filter
  ordering = ('name',)
