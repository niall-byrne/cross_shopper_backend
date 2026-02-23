"""Functions for generating admin list display column links."""

from dataclasses import dataclass
from operator import attrgetter
from typing import TYPE_CHECKING, Protocol, TypeVar, Union

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

if TYPE_CHECKING:  # no cover
  from typing import Any, Callable, Dict, Optional, Sequence, Type

  from django.db.models import Model
  from django.utils.safestring import SafeString

T = TypeVar('T', bound="admin.ModelAdmin")


@dataclass
class ColumnLinkConfig:
  """Configuration for a list display column."""

  method_name: str
  description: str
  reverse_url_name: str
  obj_id_lookup: str
  obj_name_lookup: str


@dataclass
class ColumnObjectConfig:
  """Configuration for a list display column."""

  method_name: str
  description: str
  obj_lookup: str
  is_boolean: bool = False


AliasColumnConfig = Union[ColumnLinkConfig, ColumnObjectConfig]


class ColumnGenerator(Protocol):

  def __call__(  # noqa: D102
      self,
      config: "Sequence[AliasColumnConfig]",
  ) -> None:
    ...


def column_generator(model_admin: "Type[T]") -> ColumnGenerator:
  """Generate list display columns for a model admin."""

  def get_attr_with_default(
      obj: "Model",
      lookup: "str",
  ) -> "Optional[Any]":
    """Perform attrgetter lookup, with a default 'None' value."""
    try:
      if lookup == "":
        return obj
      else:
        return attrgetter(lookup)(obj)
    except AttributeError:
      return None

  def get_html_link(
      obj: "Model",
      col: ColumnLinkConfig,
  ) -> "Optional[SafeString]":
    """Generate a html link for the given model instance and configuration."""
    obj_pk = get_attr_with_default(obj, col.obj_id_lookup)
    obj_name = get_attr_with_default(obj, col.obj_name_lookup)

    if obj_pk is None or obj_name is None:
      return None

    return format_html(
      '<a href="{}">{}</a>'.format(  # noqa: UP032
        reverse(col.reverse_url_name, args=(obj_pk,)),
        get_attr_with_default(obj, col.obj_name_lookup)
      ),
      obj_name,
    )

  def create_link_method(
      col: ColumnLinkConfig,
  ) -> "Callable[[T, Model], Optional[SafeString]]":
    return lambda _, obj: get_html_link(obj, col)

  def create_object_method(
      col: ColumnObjectConfig,
  ) -> "Callable[[T, Model], Optional[Any]]":
    return lambda _, obj: get_attr_with_default(obj, col.obj_lookup)

  mapping: "Dict[Any, Callable[[Any], Any]]" = {
      ColumnLinkConfig: create_link_method,
      ColumnObjectConfig: create_object_method,
  }

  def attach_column(config: "Sequence[AliasColumnConfig]") -> None:
    for col in config:
      create_method = mapping[col.__class__]
      method = create_method(col)
      method = admin.display(
          method,
          boolean=getattr(col, "is_boolean", False),
          description=col.description,
      )
      setattr(model_admin, col.method_name, method)

  return attach_column
