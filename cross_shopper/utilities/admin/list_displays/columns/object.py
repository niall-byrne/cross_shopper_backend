"""Configuration for a list display column containing a model."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from utilities.admin.list_displays.columns.bases.column_base import (
    ColumnConfigBase,
)

if TYPE_CHECKING:  # no cover
  from typing import Optional

  from utilities.admin.list_displays.columns.typing import AliasColumnMethod


@dataclass
class ColumnObjectConfig(ColumnConfigBase):
  """Configuration for a list display column containing a model."""

  method_name: str
  description: str
  obj_lookup: str
  obj_order: "Optional[str]" = ""
  is_boolean: bool = False

  def get_method(self) -> "AliasColumnMethod":
    """Return the method used to generate the column data."""
    return lambda _, obj: self._get_attr_with_default(obj, self.obj_lookup)

  def get_ordering(self) -> "Optional[str]":
    """Return the lookup used for column ordering."""
    if self.obj_order == "":
      return self.obj_lookup
    return self.obj_order
