"""Configuration for a list display column containing an admin link."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.urls import reverse
from django.utils.html import format_html
from utilities.admin.list_displays.columns.bases.column_base import (
    ColumnConfigBase,
)

if TYPE_CHECKING:
  from django.db.models import Model
  from django.utils.safestring import SafeString
  from utilities.admin.list_displays.columns.typing import AliasColumnMethod


@dataclass
class ColumnLinkConfig(ColumnConfigBase):
  """Configuration for a list display column containing an admin link."""

  method_name: str
  description: str
  reverse_url_name: str
  obj_id_lookup: str
  obj_name_lookup: str
  obj_order: str | None = ""

  def __str__(self) -> str:
    return self.method_name

  def get_method(self) -> AliasColumnMethod:
    """Return the method used to generate the column data."""
    return lambda _, obj: self._generate_html_link(obj)

  def _generate_html_link(
      self,
      obj: Model,
  ) -> SafeString | None:
    """Generate a html link for the given model instance and configuration."""
    obj_pk = self._get_attr_with_default(obj, self.obj_id_lookup)
    obj_name = self._get_attr_with_default(obj, self.obj_name_lookup)

    if obj_pk is None or obj_name is None:
      return None

    return format_html(
      '<a href="{}">{}</a>'.format(  # noqa: UP032
        reverse(self.reverse_url_name, args=(obj_pk,)),
        self._get_attr_with_default(obj, self.obj_name_lookup)
      ),
      obj_name,
    )

  def get_ordering(self) -> str | None:
    """Return the lookup used for column ordering."""
    if self.obj_order == "":
      return self.obj_name_lookup
    return self.obj_order
