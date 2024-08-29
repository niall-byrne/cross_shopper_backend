"""A title case transforming BlondeCharField extension."""

from typing import TypeVar

from .blonde import BlondeCharField

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")


class TitleField(BlondeCharField[_ST, _GT]):

  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
    value = super().transform(value)
    return value.capitalize()
