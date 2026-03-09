"""A django-bleach sanitizing CharField implementation."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from django.conf import settings
from django_nh3.models import Nh3CharField

if TYPE_CHECKING:
  from django.db.models import Model

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")


class BlondeCharField(Nh3CharField):
  """Adds HTML sanitization & restoration to a CharField."""

  CONFIG_KEY = "NH3_RESTORE_CONFIG"

  def pre_save(self, model_instance: Model, add: bool) -> Any:
    """Return field's value just before saving."""
    value = super().pre_save(model_instance, add)
    if value:
      for cleaned, restored in getattr(settings, self.CONFIG_KEY, {}).items():
        value = value.replace(cleaned, restored)
      setattr(model_instance, self.attname, value)
    return value
