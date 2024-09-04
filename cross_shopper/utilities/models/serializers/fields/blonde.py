"""A django-bleach sanitizing CharField implementation."""

from bleach import clean
from django.conf import settings
from django_bleach.utils import get_bleach_default_options
from utilities.models.serializers.fields.bases.transform_base import (
    TransformCharFieldBase,
)


class BlondeCharField(
    TransformCharFieldBase,
):
  """Adds HTML sanitization & restoration to a CharField."""

  CONFIG_KEY = "BLEACH_RESTORE_CONFIG"

  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
    bleach_kwargs = get_bleach_default_options()

    clean_value = clean(value, **bleach_kwargs) if value else ""

    for bleached, restored in getattr(settings, self.CONFIG_KEY, {}).items():
      clean_value = clean_value.replace(bleached, restored)

    return clean_value
