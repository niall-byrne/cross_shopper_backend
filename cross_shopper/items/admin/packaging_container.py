"""Admin for the packaging container model."""

from typing import Tuple

from django.contrib import admin
from django.http import HttpRequest
from items.models import PackagingContainer


class PackagingContainerAdmin(admin.ModelAdmin[PackagingContainer]):

  def get_ordering(self, request: HttpRequest) -> Tuple[str, ...]:
    """Return the field ordering sequence for container model instances."""
    return ('name',)
