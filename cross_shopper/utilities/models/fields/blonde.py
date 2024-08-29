"""A django-bleach sanitizing CharField implementation."""

from typing import TypeVar

from django.conf import settings
from django_bleach.models import BleachField
from .bases.transform_base import TransformCharFieldBase

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")


class BlondeCharField(
    TransformCharFieldBase[_ST, _GT],
    BleachField[_ST, _GT],
):
  """Adds HTML sanitization & restoration to a CharField."""

  CONFIG_KEY = "BLEACH_RESTORE_CONFIG"

  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
    for bleached, restored in getattr(settings, self.CONFIG_KEY, {}).items():
      value = value.replace(bleached, restored)
    return value
