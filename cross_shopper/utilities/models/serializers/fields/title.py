"""A title case transforming BlondeCharField extension."""

from .blonde import BlondeCharField


class TitleField(BlondeCharField):

  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
    value = super().transform(value)
    return value.capitalize()
