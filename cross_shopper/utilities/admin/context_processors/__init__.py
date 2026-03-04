"""Django admin template context processors."""

from typing import TYPE_CHECKING

from django.conf import settings
from django.http import HttpRequest

if TYPE_CHECKING:  # no cover
  from typing import Any, Dict


def base(_request: HttpRequest) -> "Dict[str, Any]":
  """Create the base admin site context processor."""
  return {"ENVIRONMENT": settings.ENVIRONMENT}
