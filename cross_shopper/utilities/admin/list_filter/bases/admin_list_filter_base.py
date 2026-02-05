"""Generic admin model list filter base class."""

from typing import TYPE_CHECKING, Any, List, Tuple

from django.contrib import admin

if TYPE_CHECKING:  # no cover
  from django.db import models
  from django.http import HttpRequest


class AdminListFilterBase(admin.SimpleListFilter):
  title: str
  parameter_name: str
  is_boolean: bool = False
  is_reversed: bool = False

  def queryset(
      self,
      request: "HttpRequest",
      queryset: "models.QuerySet",
  ) -> "models.QuerySet":
    """Generate a queryset to as a source for the list filter values."""
    if self.value():
      return queryset.filter(**{self.parameter_name: self.value()})
    return queryset

  def lookups(
      self,
      request: "HttpRequest",
      model_admin: "admin.ModelAdmin",
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
