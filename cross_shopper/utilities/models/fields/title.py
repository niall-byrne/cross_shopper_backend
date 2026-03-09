"""A title case transforming BlondeCharField extension."""

from typing import TypeVar

from utilities.models.fields.bases.transform_base import TransformCharFieldBase
from utilities.strings.title import TitleString
from .blonde import BlondeCharField

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")


class TitleField(  # type: ignore[misc]
    TransformCharFieldBase[_ST, _GT],
    BlondeCharField,
):
  """Adds title case transformations to the BlondeCharField."""

  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
    return TitleString(value).as_title()
