"""A serializer mixin for sanitizing input values."""

from typing import Optional

import nh3
from django.conf import settings
from django_nh3.utils import get_nh3_configured_default_options


class PeroxideFieldMixin:
  """A serializer mixin for sanitizing input values."""

  CONFIG_KEY = "NH3_RESTORE_CONFIG"

  def sanitize(self, value: Optional[str]) -> str:
    """Appliy HTML sanitization to the input value and return a safe value."""
    nh3_kwargs = get_nh3_configured_default_options()

    clean_value = nh3.clean(value, **nh3_kwargs) if value else ""

    # nh3 leaves an empty style="" if it cleans all style attributes.
    # remove it manually until ammonia/nh3 addresses it
    clean_value = clean_value.replace(
        ' style=""',
        "",
    ).replace(
        " style=''",
        "",
    )

    for cleaned, restored in getattr(settings, self.CONFIG_KEY, {}).items():
      clean_value = clean_value.replace(cleaned, restored)

    return clean_value
