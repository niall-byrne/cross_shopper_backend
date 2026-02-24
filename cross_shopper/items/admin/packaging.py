"""Admin for the packaging container model."""

from django.contrib import admin
from items.admin.list_filter.packaging import packaging_filter
from items.models import Packaging


class PackagingAdmin(admin.ModelAdmin[Packaging]):
  list_filter = packaging_filter
  ordering = ("container__name", "unit__name")
