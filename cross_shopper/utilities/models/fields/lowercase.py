"""A lowercase transforming BlondeCharField extension."""

from typing import TypeVar

from .blonde import BlondeCharField

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")


class LowerCaseField(BlondeCharField[_ST, _GT]):
  """Adds lower case transformations to the BlondeCharField."""

  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
    value = super().transform(value)
    return value.lower()
