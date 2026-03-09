"""A title case transforming BlondeCharField extension."""

from typing import TypeVar

from utilities.models.fields.bases.transform_base import TransformCharFieldBase
from .blonde import BlondeCharField

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")


class TitleField(
    TransformCharFieldBase[_ST, _GT],
    BlondeCharField[_ST, _GT],
):
  """Adds title case transformations to the BlondeCharField."""

  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
    return value.capitalize()
