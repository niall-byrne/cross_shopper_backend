"""Admin for the packaging container model."""

from django.contrib import admin
from items.admin import filters
from items.models import Packaging


class PackagingAdmin(admin.ModelAdmin[Packaging]):
  list_filter = filters.packaging_filter
  ordering = ('container__name', 'unit__name')
