"""Admin for the packaging unit model."""

from django.contrib import admin
from items.models import PackagingUnit


class PackagingUnitAdmin(admin.ModelAdmin[PackagingUnit]):
  ordering = ("name",)
