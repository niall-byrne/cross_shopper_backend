"""A lowercase transforming BlondeCharField extension."""
from __future__ import annotations

from typing import TypeVar

from utilities.models.fields.bases.transform_base import TransformCharFieldBase
from .blonde import BlondeCharField

_ST = TypeVar("_ST")
_GT = TypeVar("_GT")


class LowerCaseField(  # type: ignore[misc]
    TransformCharFieldBase[_ST, _GT],
    BlondeCharField,
):
  """Adds lower case transformations to the BlondeCharField."""

  def transform(self, value: str) -> str:
    """Transform the field value into a new form."""
    return value.lower()
