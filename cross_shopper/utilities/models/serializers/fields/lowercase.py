"""A lowercase transforming BlondeCharField extension."""

from .blonde import BlondeCharField


class LowerCaseField(BlondeCharField):
  """Adds lower case transformations to the BlondeCharField."""

  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
    value = super().transform(value)
    return value.lower()
