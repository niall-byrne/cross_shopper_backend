"""Generic admin model list filter base class."""

from typing import TYPE_CHECKING

from django.contrib import admin

if TYPE_CHECKING:  # no cover
  from django.db import models
  from django.http import HttpRequest


class AdminListFilterBase(admin.SimpleListFilter):
  title: str
  parameter_name: str
  reverse: bool = False

  def queryset(self, request: "HttpRequest", queryset: "models.QuerySet"):
    """Generate a queryset to as a source for the list filter values."""
    if self.value():
      return queryset.filter(**{self.parameter_name: self.value()})
    return queryset

  def lookups(self, request: "HttpRequest", model_admin: "admin.ModelAdmin"):
    """Generate a list of filter tuples from the configured query set."""
    qs = model_admin.get_queryset(request)
    operator = "-" if self.reverse else ""
    names = qs.values_list(
        self.parameter_name,
        flat=True,
    ).distinct().order_by(operator + self.parameter_name)
    return [(name, name) for name in names]
