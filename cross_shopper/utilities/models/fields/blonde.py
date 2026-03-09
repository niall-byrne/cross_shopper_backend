"""A django-bleach sanitizing CharField implementation."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from django.conf import settings
from django_bleach.models import BleachField

if TYPE_CHECKING:
  from django.db.models import Model

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")


class BlondeCharField(BleachField[_ST, _GT]):
  """Adds HTML sanitization & restoration to a CharField."""

  CONFIG_KEY = "BLEACH_RESTORE_CONFIG"

  def pre_save(self, model_instance: Model, add: bool) -> Any:
    """Return field's value just before saving."""
    value = super().pre_save(model_instance, add)
    if value:
      for bleached, restored in getattr(settings, self.CONFIG_KEY, {}).items():
        value = value.replace(bleached, restored)
      setattr(model_instance, self.attname, value)
    return value
