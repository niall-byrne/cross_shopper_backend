"""Generic admin model list filter base class."""

from typing import TYPE_CHECKING, Any, List, Tuple, Type

from django.contrib import admin

if TYPE_CHECKING:  # no cover
  from django.db import models
  from django.http import HttpRequest


class GenericListFilter(admin.SimpleListFilter):
  title: str
  parameter_name: str
  is_boolean: bool = False
  is_reversed: bool = False

  @classmethod
  def create(
      cls,
      title: str,
      parameter_name: str,
      is_boolean: bool = False,
      is_reversed: bool = False,
  ) -> Type["GenericListFilter"]:
    """Generate a subclass to use as a SimpleListFilter."""
    args = {
        "title": title,
        "parameter_name": parameter_name,
        "is_boolean": is_boolean,
        "is_reversed": is_reversed,
    }

    class Generated(GenericListFilter):
      title = str(args["title"])
      parameter_name = str(args["parameter_name"])
      is_boolean = bool(args["is_boolean"])
      is_reversed = bool(args["is_reversed"])

    return Generated

  def queryset(
      self,
      request: "HttpRequest",
      queryset: "models.QuerySet[Any]",
  ) -> "models.QuerySet[Any]":
    """Generate a filtered queryset as the result of the filter operation."""
    if self.value():
      return queryset.filter(**{self.parameter_name: self.value()})

    return queryset

  def lookups(
      self,
      request: "HttpRequest",
      model_admin: "admin.ModelAdmin[Any]",
  ) -> List[Tuple[Any, Any]]:
    """Generate a list of filter tuples from the configured query set."""
    if self.is_boolean:
      return self.boolean_lookups()

    qs = model_admin.get_queryset(request)

    operator = "-" if self.is_reversed else ""
    names = qs.values_list(
        self.parameter_name,
        flat=True,
    ).distinct().order_by(operator + self.parameter_name)
    return [(name, name) for name in names]

  def boolean_lookups(self) -> List[Tuple[bool, str]]:
    """Generate a list of filter tuples for boolean filter values."""
    values = [(True, "Yes"), (False, "No")]

    if self.is_reversed:
      values.reverse()

    return values
