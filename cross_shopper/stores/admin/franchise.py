"""Admin for the franchise model."""

from django.contrib import admin
from stores.models import Franchise

from . import filters


class FranchiseAdmin(admin.ModelAdmin[Franchise]):
  list_filter = filters.franchise_filter
  ordering = ('name',)
