"""Admin for the franchise model."""

from django.contrib import admin
from stores.admin import filters
from stores.models import Franchise


class FranchiseAdmin(admin.ModelAdmin[Franchise]):
  list_filter = filters.franchise_filter
  ordering = ('name',)
