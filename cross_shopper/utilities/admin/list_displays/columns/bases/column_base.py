"""Base configuration for a list display column containing a model."""
from __future__ import annotations

from abc import ABC, abstractmethod
from operator import attrgetter
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
  from django.db.models import Model
  from utilities.admin.list_displays.columns.typing import AliasColumnMethod


class ColumnConfigBase(ABC):
  """Base configuration for a list display column containing a model."""

  method_name: str

  _default_order = "obj_order"

  def _get_attr_with_default(
      self,
      obj: Model,
      lookup: str,
  ) -> Any | None:
    try:
      if lookup == "":
        return obj
      else:
        return attrgetter(lookup)(obj)
    except AttributeError:
      return None

  @abstractmethod
  def get_method(self) -> AliasColumnMethod:
    """Return the method used to generate the column data."""

  @abstractmethod
  def get_ordering(self) -> str | None:
    """Return the lookup used for column ordering."""

  def __str__(self) -> str:
    return self.method_name
