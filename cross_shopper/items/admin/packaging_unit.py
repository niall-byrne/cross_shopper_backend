"""Admin for the packaging unit model."""

from typing import Tuple

from django.contrib import admin
from django.http import HttpRequest
from items.models import PackagingUnit


class PackagingUnitAdmin(admin.ModelAdmin[PackagingUnit]):

  def get_ordering(self, request: HttpRequest) -> Tuple[str, ...]:
    """Return the field ordering sequence for unit model instances."""
    return ('name',)
