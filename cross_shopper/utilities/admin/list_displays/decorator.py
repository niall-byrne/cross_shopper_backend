"""Function for generating model admin list display column entries."""

from typing import TYPE_CHECKING

from django.contrib import admin

if TYPE_CHECKING:  # no cover
  from typing import List, Type

  from utilities.admin.list_displays.columns.typing import (
      AliasConfiguration,
      ColumnGenerator,
      T,
  )


def generate_list_display(config: "AliasConfiguration") -> "ColumnGenerator":
  """Generate list display columns for a model admin."""

  def attach_list_display_method(model_admin: "Type[T]") -> "Type[T]":

    list_display: "List[str]" = []

    for col in config:
      if isinstance(col, str):
        list_display.append(col)
        continue

      ordering = col.get_ordering()
      if isinstance(ordering, str):
        ordering = ordering.replace(".", "__")

      method = admin.display(
          col.get_method(),
          boolean=getattr(col, "is_boolean", False),
          description=col.description,
          ordering=ordering,
      )
      setattr(model_admin, col.method_name, method)
      list_display.append(col.method_name)

    setattr(model_admin, "list_display", tuple(list_display))

    return model_admin

  return attach_list_display_method
