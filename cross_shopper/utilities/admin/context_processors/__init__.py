"""Django admin template context processors."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.conf import settings

if TYPE_CHECKING:
  from django.http import HttpRequest


def base(_request: HttpRequest) -> dict[str, Any]:
  """Create the base admin site context processor."""
  return {"ENVIRONMENT": settings.ENVIRONMENT}
