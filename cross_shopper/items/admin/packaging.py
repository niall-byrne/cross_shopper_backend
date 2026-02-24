"""Admin for the packaging container model."""

from django.contrib import admin
from items.models import Packaging

from . import filters


class PackagingAdmin(admin.ModelAdmin[Packaging]):
  list_filter = filters.packaging_filter
  ordering = ('container__name', 'unit__name')
