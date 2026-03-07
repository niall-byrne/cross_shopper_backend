"""A django-bleach sanitizing CharField implementation."""

from utilities.models.serializers.fields.bases.transform_base import (
    TransformCharFieldBase,
)
from utilities.models.serializers.fields.mixins.peroxide import (
    PeroxideFieldMixin,
)


class BlondeCharField(
    TransformCharFieldBase,
    PeroxideFieldMixin,
):
  """Adds HTML sanitization & restoration to a CharField."""

  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
    return self.sanitize(value)
