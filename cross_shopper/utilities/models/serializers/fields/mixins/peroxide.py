"""A serializer mixin for sanitizing input values."""

from bleach import clean
from django.conf import settings
from django_bleach.utils import get_bleach_default_options


class PeroxideFieldMixin:
  """A serializer mixin for sanitizing input values."""

  CONFIG_KEY = "BLEACH_RESTORE_CONFIG"

  def sanitize(self, value: str | None) -> str:
    """Appliy HTML sanitization to the input value and return a safe value."""
    bleach_kwargs = get_bleach_default_options()

    clean_value = clean(value, **bleach_kwargs) if value else ""

    for bleached, restored in getattr(settings, self.CONFIG_KEY, {}).items():
      clean_value = clean_value.replace(bleached, restored)

    return clean_value
