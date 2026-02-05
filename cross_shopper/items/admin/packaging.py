"""Admin for the packaging container model."""

from django.contrib import admin
from items.models import Packaging


class PackagingAdmin(admin.ModelAdmin[Packaging]):
  ordering = ('container__name', 'unit__name')
